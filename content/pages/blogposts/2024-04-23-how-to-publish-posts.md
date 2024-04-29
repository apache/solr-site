Title: How To: Contribute to the Apache Solr Blog
category: solr/blogposts
URL: blogposts/contribute-to-the-apache-solr-blog.html
save_as: blogposts/contribute-to-the-apache-solr-blog.html
slug: contribute-to-the-apache-solr-blog
summary: You have a brilliant idea for Solr's new blog.  But what next?  How does the blog work, and how can writers contribute posts?

# Inspiration Strikes!

Digging through the ref-guide to address a tricky query-side problem for a customer, you just discovered a hidden gem in Solr's query language.
"Solr can do graph queries?" you ask your monitor incredulously - "why don't more people know about this?"
"Why didn't **I** know about this?"

You'd like to highlight this for other users that might be missing out, but how?
An email to the [Solr User mailing list](https://solr.apache.org/community.html#mailing-lists-irc) feels too ephemeral.
And the Reference Guide, which focuses on syntax and mechanics, seems too technical and abstract for what you'd imagined writing.

The newly-introduced Apache Solr Blog seems like the perfect way to share this sort of content with the Solr community.
You fire up your editor and put together a first draft you're really excited about.
It's ready to go - you've even come up with a pun-based title: _"Solr's Real Graphical User Interface"_

But what next?
How do blog posts get on [solr.apache.org](https://solr.apache.org)?

### Disclaimers, Scope, and Caveats

This walkthrough aims to cover the process of contributing a post for the [solr.apache.org](https://solr.apache.org) blog.
Basic familiarity with some tools, particularly Git and Github, is assumed for the purposes of this tutorial.
There are a handful of really great primers out there that cover these better than we could hope to here.
A few links for reference:

* [An interactive, sandbox-based Git Tutorial](https://learngitbranching.js.org/)
* [Git's Project Documentation](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
* [Github Docs Landing Page](https://docs.github.com/en/get-started)

Of course, questions from potential contriubtors are always welcome: try the development mailing list, Slack, or IRC channels listed [here](https://solr.apache.org/community.html) if you have any problems.

With those caveats out of the way, let's contribute our first blog post!

# Setup - Getting the Website Code

All content on Solr's website is maintained in a git repository called [solr-site](https://github.com/apache/solr-site).
Nearly everything you can read on [solr.apache.org](https://solr.apache.org) comes from one or more text files in this repo.
Blog posts are no exception: each post on our blog is "just" a Markdown-formatted text file.

So the first step in sharing your writeup is to get a copy of this repo to work with.
You haven't edited the Solr website before, so you create a local "clone" (i.e. copy) of `solr-site`, "fork" the repo in Github (not shown below), register your Github "fork" as a "remote", and create a "branch" locally to put your changes on.

```
$ git clone git@github.com:apache/solr-site.git
$ git remote add myGHfork git@github.com:myGHusername/solr-site.git
$ git checkout -b blog-post-highlighting-graph-query
```

# First Edits - Creating a File For your Post

All blog posts are expected to live in the `content/pages/blogposts` directory of the repo.
Additionally, the filename for each post is expected to follow a particular format.
Filenames start with a date (in `YYYY-MM-DD` format), continue with a short identifier or description, and conclude with the `.md` suffix (used to signify a Markdown file).

The date portion of the filename is used to order posts in the blog's RSS feed, and as a "published date" that appears on each article.
Authors should generally pick the current date, unless they have a good guess when their article may appear publicly.
If the review process (more on this below) takes longer than expected, authors or reviewers may update this date as necessary.

Images or other static files used by your post can be placed in `content/images/blog/` and referenced with Markdown syntax like `![Alt Text]({static}/images/blog/imageFileName.png)`

Knowing all this, you create a new file at `content/pages/blogposts/2024-04-23-graph-query-is-great.md` and copy in the draft text you've been working on.
When finished, it appears as:

```
$ git status
On branch blog-post-highlighting-graph-query
Untracked files:
  (use "git add <file>..." to include in what will be committed)
    content/pages/blogposts/2024-04-23-graph-query-is-great.md
$ cat content/pages/blogposts/2024-04-23-graph-query-is-great.md
<b>Lorem ipsum</b>
dolor sit amet,
consectetur adipiscing elit.
```

# Formatting

## Markdown

Your post content is in the right place, but you realize now that you used HTML tags in some places instead of the Markdown syntax that is required.
Using a [Markdown "Cheat-Sheet"](https://www.markdownguide.org/cheat-sheet/) as a guide, you reformat your post as necessary.
Looking much better now!

## Pelican Metadata

Solr uses a tool called [Pelican](https://getpelican.com/) to turn the text and Markdown files in the repo into the website that readers can view at [solr.apache.org](https://solr.apache.org/).
When parsing files, Pelican requires certain bits of metadata at the top of each content file.
This metadata helps Pelican know what to do with each file, and help it differentiate between types of content so that each can be rendered correctly.

Pelican requires the following metadata tags on each blog post:

* **category** - for blogposts, should always the literal value "solr/blogposts"
* **Title** - a user-facing title for your post, to appear in RSS and at the top of your post.  May contain spaces, etc.
* **slug** - an identifier for your page, meant to be unique across all pages on [solr.apache.org](https://solr.apache.org).  Often used in `save_as` and `URL` properties (see below).
* **save_as** - the filename for Pelican to use for the HTML file generated for your blog post.  Should typically be `blogposts/<slug-value>.html`
* **URL** - the URL your blog post will be hosted at, relative to the root of the site.  Should typically match the `save_as` value (see above) i.e. `blogposts/<slug-value>.html`

Pelican supports other non-required fields as well.
Notable among these is **summary**, which Solr's blog displays as a short blurb under article titles on the Blog's landing page.
(The first few sentences will be chosen for this by default, if no explicit summary value is specified.)
For more information on valid metadata values, see the Pelican docs [here](https://docs.getpelican.com/en/latest/content.html#file-metadata).

You tweak your blog post title one last time, and add the necessary metadata at the top of `2024-04-23-graph-query-is-great.md`:

```
$ cat content/pages/blogposts/2024-04-23-graph-query-is-great.md
Title: 'Node'-doubt about it; Solr 'Edges' Out the Rest!
category: solr/blogposts
slug: highlight-graph-query
URL: blogposts/highlight-graph-query.html
save_as: blogposts/highlight-graph-query.html

## Lorem ipsum
dolor sit amet,
consectetur adipiscing elit.
```

# Previewing your Work

With the proper formatting in place your post _should_ be ready to appear on the blog, but it's worth checking locally to catch any potential issues before putting it in front of others for review.

Luckily, Pelican  makes it easy to validate changes by building the Solr website locally.

Excited to see your Graph Query post rendered, you go to the repository root and run `./build.sh -l`.
This invokes Pelican to build the website, and spins up a web server (on port 8000) to make the pages available.
You type `http://localhost:8000/blog.html` in your browser of choice to preview the landing page of the blog.
Sure enough - there it is, right there in the list of recent posts:

![Graph Query Blog Post Preview]({static}/images/blog/graph-query-blog-preview.png)

Clicking on the article link, you're taken to your post's page.
It's gorgeous - there are a few Markdown syntax errors, but otherwise it looks great.
When you fix the syntax errors, Pelican detects the changes and rebuilds the site automatically, allowing you to see the fixes in your browser with just a "Refresh".

You're ready to publish for review!

# Sharing with Others

First, you push your changes up to the Github "fork" you created earlier:

```
$ git add -A
$ git commit -m "Add a blog post about Solr's graph query support"
$ git push myGHfork blog-post-highlighting-graph-query:blog-post-highlighting-graph-query
```

With that done, you open the GitHub [solr-site](https://github.com/apache/solr-site) page in your browser and create a PR from the `blog-post-highlighting-graph-query` branch now available on your Github fork.
Several days later the PR receives positive review ("LGTM - I loved the puns!") and is merged.
You've done it - you've taken your Graph Query evangelism from initial idea to published post!

# Conclusion

This post aims to show that contributing to [solr.apache.org](https://solr.apache.org) is as straightforward and painless as possible.  Blog posts:

* live alongside the rest of Solr's website
* use the ubiquitous Markdown syntax for formatting
* can be rendered and tested locally with a single command, and ...
* are shared and reviewed using the same PR-based process the community already uses to manage documentation and code changes.

This lack of friction should allow the whole community to make their voices heard!
Here's hoping the next post the community reads, is yours!
