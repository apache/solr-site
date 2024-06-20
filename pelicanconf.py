#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime, date
#from checksumdir import dirhash

AUTHOR = 'Solr Developers'
SITENAME = 'Apache Solr'
SITESUBTITLE = ''
SITEURL = ''
CURRENTYEAR = date.today().year

SOLR_LATEST_RELEASE = '9.6.1'
SOLR_LATEST_RELEASE_DATE = datetime(2024, 5, 29)
SOLR_PREVIOUS_MAJOR_RELEASE = '8.11.3'

SOLR_OPERATOR_LATEST_RELEASE = 'v0.8.1'
SOLR_OPERATOR_LATEST_RELEASE_DATE = datetime(2024, 4, 12)
SOLR_OPERATOR_PREVIOUS_MAJOR_RELEASE = 'v0.7.1'

# This string will be appended to all unversioned css and js resources to prevent caching surprises on edits.
# The theme's htaccess file also sets a cache-control header with longer lifetime, if the v=XXXX query string is added.
#STATIC_RESOURCE_SUFFIX = "?v=%s" % dirhash('themes/solr/static', 'sha1')[-8:]
# SOLR-17339: Dynamic hash disabled until we can install custom modules like checksumdir. Bump this manually on changes
STATIC_RESOURCE_SUFFIX = "?v=4dd59757"

PATH = 'content'

THEME = 'themes/solr'

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

# GOOGLE_ANALYTICS_TRACKING_ID = 'G-QKSF79B9Y1'

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

EXTRA_PATH_METADATA = {}

STATIC_PATHS = ['.']

TEMPLATE_PAGES = {'htaccess.template': '.htaccess'}

PLUGIN_PATHS = ['./plugins']
PLUGINS = [
    'extract_toc',
    'jinja2content',
    'regex_replace',
    'age_days_lt',
# SOLR-17339: Vex disabled until https://github.com/apache/infrastructure-actions/pull/63 is merged
#    'vex'
#    'md_inline_extension',
]

MARKDOWN = {
    'extension_configs': {
        'toc': {},
        'markdown.extensions.codehilite': {'css_class': 'codehilite'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}
