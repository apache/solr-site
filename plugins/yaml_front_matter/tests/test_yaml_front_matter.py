import unittest

from markdown.preprocessors import Preprocessor
from markdown import Markdown

from plugins.yaml_front_matter.yaml_front_matter import YamlFrontMatterPreprocessor


class TestYamlFrontMatterPreprocessor(unittest.TestCase):

    def __create_preprocessor(self) -> Preprocessor:
        md = Markdown()
        preprocessor: Preprocessor = YamlFrontMatterPreprocessor(md)
        self.assertTrue(hasattr(preprocessor, "md"))
        return YamlFrontMatterPreprocessor(md)

    def test_removes_yaml_front_matter(self):
        preprocessor: Preprocessor = self.__create_preprocessor()
        input_text: list[str] = [
            "---",
            "title: Test Title",
            "date: 2024-06-01",
            "number: 42",
            "---",
            "Content starts here."
        ]
        expected_meta: dict = {"title": "Test Title", "date": "2024-06-01", "number": "42"}
        expected_output = ["Content starts here."]
        output = preprocessor.run(input_text)
        self.assertTrue(hasattr(preprocessor.md, "Meta"))
        self.assertEqual(preprocessor.md.Meta, expected_meta)
        self.assertEqual(output, expected_output)

    def test_no_front_matter(self):
        preprocessor: Preprocessor = self.__create_preprocessor()
        input_text = ["No front matter here."]
        output = preprocessor.run(input_text)
        self.assertFalse(hasattr(preprocessor.md, "Meta"))
        self.assertEqual(output, input_text)

    def test_partial_front_matter(self):
        preprocessor: Preprocessor = self.__create_preprocessor()
        input_text = [
            "---",
            "title: Only start delimiter"
        ]
        output = preprocessor.run(input_text)
        self.assertFalse(hasattr(preprocessor.md, "Meta"))
        self.assertEqual(output, input_text)

    def test_invalid_yaml_front_matter(self):
        preprocessor: Preprocessor = self.__create_preprocessor()
        input_text = [
            "---",
            "title: [Unclosed list",
            "---",
            "Content after invalid YAML."
        ]
        output = preprocessor.run(input_text)
        self.assertFalse(hasattr(preprocessor.md, "Meta"))
        self.assertEqual(output, input_text)
