#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Lucene and Solr Developers'
SITENAME = 'Apache Lucene'
SITEURL = ''

PATH = 'content'

THEME = 'themes/lucene'

TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'

DEFAULT_DATE_FORMAT = '%-d %B %Y'
DATE_FORMATS = {
    'en': '%-d %B %Y',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

EXTRA_PATH_METADATA = {
    'pages/core/corenews.md': {
        'url': 'core/',
        'save_as': 'core/corenews.html',
        },
    }
PLUGIN_PATHS = ['./plugins']
PLUGINS = [
    'extract_toc',
    'jinja2content',
    'md_inline_extension',
]

MARKDOWN = {
    'extension_configs': {
        'toc': {},
        'mdx_include': {},
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}
