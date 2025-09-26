from markdown import Markdown
from markdown.extensions import Extension
from markdown.extensions.meta import BEGIN_RE, END_RE
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from pelican import Readers
from pelican.plugins import signals
from strictyaml import load
from strictyaml.ruamel import YAMLError
from typing import Any
import logging


YAML_FRONT_MATTER_EXTENSION_NAME = 'yaml_front_matter:YamlFrontMatterExtension'
YAML_FRONT_MATTER_ATTRIBUTE = 'yaml_front_matter'

#
# We need to implement both a preprocessor and a postprocessor, because the `meta` extension
# modifies the `Meta` attribute of the Markdown instance, which we want to preserve.
#
class YamlFrontMatterPreprocessor(Preprocessor, Postprocessor):
    """ Preprocessor to handle YAML front matter in Markdown files. """

    def run(self, arg: str | list[str]) -> Any:
        if isinstance(arg, str):
            return self.postprocess(arg)
        else:
            return self.preprocess(arg)

    def preprocess(self, lines: list[str]) -> list[str]:
        """ Parse Meta-Data and store in Markdown.Meta. """
        if self.md is not None and hasattr(self.md, YAML_FRONT_MATTER_ATTRIBUTE):
            delattr(self.md, YAML_FRONT_MATTER_ATTRIBUTE)
        front_matter_lines: list[str] = []
        if lines and BEGIN_RE.match(lines[0]):
            copy: list[str] = lines.copy()
            # Remove the first line if it matches the BEGIN_RE
            copy.pop(0)
            while copy:
                line = copy.pop(0)
                if END_RE.match(line):
                    # Join the front matter lines and parse them as YAML
                    raw_yaml = "\n".join(front_matter_lines)
                    try:
                        parsed = load(raw_yaml)
                        data = parsed.data
                        for v in data.values():
                            if len(v) == 1 and isinstance(v, dict):
                                # Workaround an Article limitation that treats metadata values with length 1 as lists
                                v.setdefault('0', '')
                        if self.md is not None:
                            # Save the metadata to be restored in postprocessing
                            setattr(self.md, YAML_FRONT_MATTER_ATTRIBUTE, data)
                        return copy
                    except YAMLError as e:
                        logging.warning("Invalid YAML front matter: %s", e)
                front_matter_lines.append(line)
        # Return the original lines if no YAML front matter is found
        return lines

    def postprocess(self, text: str) -> str:
        if self.md is not None and hasattr(self.md, YAML_FRONT_MATTER_ATTRIBUTE):
            # Reset the metadata broken by the `meta` extension
            self.md.Meta = getattr(self.md, YAML_FRONT_MATTER_ATTRIBUTE)
        return text

class YamlFrontMatterExtension(Extension):
    """ Extension to add YAML front matter support to Markdown. """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.md = None

    def extendMarkdown(self, md: Markdown):
        md.registerExtension(self)
        self.md = md
        # Uses a higher priority than the default `meta` extension
        processor = YamlFrontMatterPreprocessor(md)
        md.preprocessors.register(processor, "yaml_front_matter", 28)
        md.postprocessors.register(processor, "yaml_front_matter", 0)

    def reset(self) -> None:
        if self.md is not None:
            # Reset the Meta data to an empty dictionary
            self.md.Meta = {}

def initialize_readers(readers: Readers):
    """Initialize the readers with the YAML front matter extension."""
    extensions: list[str] = readers.settings.setdefault("MARKDOWN", {}).setdefault("extensions", [])
    # Register the YAML front matter extension if not already registered
    if YAML_FRONT_MATTER_EXTENSION_NAME not in extensions:
        extensions.append(YAML_FRONT_MATTER_EXTENSION_NAME)


def register():
    """Plugin registration"""
    signals.readers_init.connect(initialize_readers)
