import unittest
from unittest.mock import MagicMock, patch, mock_open

from contextlib import contextmanager
from pelican import Readers
from pelican.readers import BaseReader, MarkdownReader

from plugins.yaml_front_matter import yaml_front_matter


class TestProcessorOrder(unittest.TestCase):

    @staticmethod
    def __create_settings() -> dict:
        """Create a settings dictionary for the test."""
        return {
            'CACHE_PATH': '.',
            'CHECK_MODIFIED_METHOD': 'mtime',
            'FORMATTED_FIELDS': [],
            'GZIP_CACHE': False,
            'READERS': {},
        }

    def test_yaml_front_matter_before_meta(self):
        # Register readers and processors
        yaml_front_matter.register()
        readers: Readers = Readers(self.__create_settings())
        markdown_reader: BaseReader = readers.readers['md']
        self.assertTrue(isinstance(markdown_reader, MarkdownReader), "MarkdownReader should be registered")
        # Simulate reading the Markdown content
        with patch('pelican.readers.pelican_open', fake_pelican_open):
            content, meta = markdown_reader.read("test.md")
            expected_meta: dict = {
                'nested': {
                    'number': "42",
                    'string': "forty-two"
                }
            }
            self.assertEqual(expected_meta, meta, "Meta data should match the YAML front matter")
            self.assertEqual('<p>Test content with YAML front matter.</p>', content)


@contextmanager
def fake_pelican_open(*args, **kwargs):
    """Context manager to simulate reading a file with YAML front matter."""
    yield """---
nested:
  number: 42
  string: "forty-two"
---
Test content with YAML front matter."""
