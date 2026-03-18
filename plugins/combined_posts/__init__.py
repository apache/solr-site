"""
Pelican plugin to generate a combined posts page with pagination.

Combines articles (solr/news, solr/security) with pages (solr/blogposts),
sorts them chronologically, and generates paginated output.
"""

from pelican import signals
from pelican.generators import Generator
from pelican.paginator import Paginator
from pelican.writers import Writer
import os
import logging

logger = logging.getLogger(__name__)


class CombinedPostsGenerator(Generator):
    """
    Generator for creating a combined posts page with pagination.

    Combines articles from 'solr/news' and 'solr/security' categories
    with pages from 'solr/blogposts' category, sorts chronologically,
    and generates paginated HTML pages.
    """

    def generate_output(self, writer):
        """Generate paginated combined posts pages."""

        # Get all articles and pages
        articles = self.context.get('articles', [])
        pages = self.context.get('pages', [])

        # Filter and combine
        # Include articles from news and security categories
        combined_articles = [
            a for a in articles
            if hasattr(a, 'category') and a.category and
               a.category.name in ['solr/news', 'solr/security']
        ]

        # Include pages from blogposts category
        combined_pages = [
            p for p in pages
            if hasattr(p, 'category') and p.category and
               p.category.name == 'solr/blogposts'
        ]

        # Combine all
        combined_posts = combined_articles + combined_pages

        # Sort by date, newest first
        combined_posts.sort(key=lambda x: x.date, reverse=True)

        # Get pagination settings
        per_page = self.settings.get('COMBINED_POSTS_PER_PAGE', 20)

        # Create paginator
        paginator = Paginator('posts', 'posts{number}.html',
                              combined_posts, self.settings, per_page)

        # Get the template
        template = self.get_template('posts')

        # Generate each page
        for page_num in range(1, paginator.num_pages + 1):
            posts_page = paginator.page(page_num)

            # Build context
            context = self.context.copy()
            context.update({
                'posts': posts_page.object_list,
                'posts_page': posts_page,
                'posts_paginator': paginator,
                'page': posts_page,  # For breadcrumb/metadata
                'title': 'Posts',
                'slug': 'posts',
            })

            # Determine output path
            if page_num == 1:
                output_path = os.path.join(self.output_path, 'posts.html')
                url = 'posts.html'
            else:
                output_path = os.path.join(
                    self.output_path,
                    f'posts{page_num}.html'
                )
                url = f'posts{page_num}.html'

            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Render and write
            output = template.render(context)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)

            # Log
            logger.info(f'Writing {url} ({page_num}/{paginator.num_pages})')


def get_generators(pelican):
    """Register the CombinedPostsGenerator."""
    return CombinedPostsGenerator


def register():
    """Plugin registration hook."""
    signals.get_generators.connect(get_generators)
