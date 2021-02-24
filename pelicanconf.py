#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime, date
from checksumdir import dirhash

AUTHOR = 'Lucene and Solr Developers'
SITENAME = 'Apache Lucene'
SITESUBTITLE = ''
SITEURL = ''
CURRENTYEAR = date.today().year

LUCENE_LATEST_RELEASE = '8.8.1'
LUCENE_LATEST_RELEASE_DATE = datetime(2021, 2, 22)
LUCENE_PREVIOUS_MAJOR_RELEASE = '7.7.3'

# This string will be appended to all unversioned css and js resources to prevent caching surprises on edits.
# The theme's htaccess file also sets a cache-control header with longer lifetime, if the v=XXXX query string is added.
STATIC_RESOURCE_SUFFIX = "?v=%s" % dirhash('themes/lucene/static', 'sha1')[-8:]

PATH = 'content'

THEME = 'themes/lucene'

TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'

DEFAULT_DATE_FORMAT = '%-d %B %Y'
DATE_FORMATS = {
    'en': '%-d %B %Y',
}

USE_FOLDER_AS_CATEGORY = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

INDEX_SAVE_AS = ''
ARTICLE_SAVE_AS = ''
ARTICLE_LANG_SAVE_AS = ''
DRAFT_SAVE_AS = ''
DRAFT_LANG_SAVE_AS = ''
PAGE_SAVE_AS = ''
PAGE_LANG_SAVE_AS = ''
TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
CATEGORY_SAVE_AS = ''

SLUG_REGEX_SUBSTITUTIONS = [
(r'[^\w\s-]', ''), # remove non-alphabetical/whitespace/'-' chars
(r'(?u)\A\s*', ''), # strip leading whitespace
(r'(?u)\s*\Z', ''), # strip trailing whitespace
(r'[-\s]+', '-'), # reduce multiple whitespace or '-' to single '-'
]

CATEGORY_REGEX_SUBSTITUTIONS = []

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

GOOGLE_ANALYTICS_TRACKING_ID = 'UA-94576-12'

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

EXTRA_PATH_METADATA = {
    'pages/core/corenews.md': {
        'url': 'core/',
        'save_as': 'core/corenews.html',
        },
    }

STATIC_PATHS = ['.']

TEMPLATE_PAGES = {'htaccess.template': '.htaccess'}

PLUGIN_PATHS = ['./plugins']
PLUGINS = [
    'extract_toc',
    'jinja2content',
    'regex_replace',
    'age_days_lt'
#    'md_inline_extension',
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
