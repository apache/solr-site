Title: How To - Contribute to the Apache Solr Blog
category: solr/blogposts
URL: blogposts/contribute-to-the-apache-solr-blog.html
save_as: blogposts/contribute-to-the-apache-solr-blog.html
slug: contribute-to-the-apache-solr-blog
summary: You have a brilliant idea for Solr's new blog.  But what next?  How do you contribute a post to Solr's blog?

Digging through the ref-guide to address a tricky query-side problem for a client, you just discovered a hidden gem in Solr's query language: the [Graph Query Parser](https://solr.apache.org/guide/solr/latest/query-guide/other-parsers.html#graph-query-parser)!
"Solr can do graph queries?" you ask your monitor incredulously - "why don't more people know about this?"
"Why didn't **I** know about this?"

Frustrated that you've been missing out, you'd like to highlight this for other users that might be in a similar situation.
But how?
An email to the [Solr User mailing list](https://solr.apache.org/community.html#mailing-lists-irc) feels too ephemeral.
And the Reference Guide, where the focus is on syntax and technical documentation, doesn't quite seem to fit your goal either.

The answer - the newly-introduced Apache Solr Blog - is the perfect way to share with the Solr community whether your post is about a recent contribution, a vibrant community event, or a use-case you think is overlooked.

You fire up `$EDITOR` and put together a first draft you're really excited about.
It's ready to go - you've even come up with a pun-based title: "Solr's Real 'Graph'ical User Interface"
But what next?
How do you contribute a Solr blog post?

## Disclaimers, Scope, and Caveats

Of course, this walkthrough can't cover every nuance of the tools and techniques required.
Basic familiarity with some tools, particularly Git and Github, is assumed for the purposes of this tutorial.
There are a handful of really great primers out there, that cover Git and Github better than we could hope to here.
A few links for reference:

* [An interactive, sandbox-based Git Tutorial](https://learngitbranching.js.org/)
* [Git's Project Documentation](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
* [Github Docs Landing Page](https://docs.github.com/en/get-started)

If you can't find answers to your `git` questions elsewhere, or have project-specific questions about our git/GitHub process, try the development mailing list, Slack, or IRC channels listed [here](https://solr.apache.org/community.html).
We're always happy to help potential contributors!

With those caveats out of the way, let's contribute our first blog post!

## Detailed Walkthrough

### Setup - Getting the Website Code

All content on Solr's website is maintained in a "git" repository called [solr-site](https://github.com/apache/solr-site).
Nearly everything you can read on `solr.apache.org` comes from one or more text files in this repository.
Blog posts are no exception: each post on the Apache Solr Blog is "just" a Markdown-formatted text file in this repository.
So the first step in sharing your writeup (now titled: "Warning: Graphic Content"), is to get a copy of this repository to work with.
You haven't edited the Solr website before, so you create a local "clone" (i.e. copy) of `solr-site`, "fork" the repository in Github (not shown below), register your Github "fork" as a "remote", and create a "branch" locally to put your changes on.

```
$ git clone git@github.com:apache/solr-site.git
$ git remote add myGHfork git@github.com:myGHusername/solr-site.git
$ git checkout -b blog-post-highlighting-graph-query
```

### First Edits - Creating a File For your Post

Now that you have the website code locally, you create a file to contain your post.
You know where to put it - blog posts live in the `content/pages/blogposts` directory in the repo.
The file name though is a bit trickier.

Solr relies on a few conventions in how files are named that contain blog posts and other news items that appear on its site.
In particular, filenames start with a date (in `YYYY-MM-DD` format), continue with a short identifier or description, and conclude with the `.md` suffix often used with Markdown files.
The date portion of the filename is used to order posts in the blog's RSS feed, and as a "published date" that appears on each article.
Authors should generally pick the current date, unless they have a good guess when their article may appear publicly.
If the review process (more on this below) takes longer than expected, authors or reviewers may update this date as necessary.

You open `$EDITOR`, create a new file `content/pages/blogposts/2024-04-23-graph-query-is-great.md`, and paste in your draft.
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

Images, if you wanted to include any, can be placed in `content/images/blog/` and referenced with Markdown syntax like `![Alt Text]({static}/images/blog/imageFileName.png)`

### Formatting

#### Markdown

Your post content is in the right place, but you realize now that you used HTML tags in some places instead of the Markdown syntax that is required.
Using a [Markdown "Cheat-Sheet"](https://www.markdownguide.org/cheat-sheet/) as a guide, you reformat your post as necessary.
Looking much better now!

#### Pelican Metadata

Solr uses a tool called [Pelican](https://getpelican.com/) to turn the text and Markdown files you see in [solr-site](https://github.com/apache/solr-site) into the website that readers can view at [solr.apache.org](https://solr.apache.org/).
When parsing files, Pelican requires certain bits of metadata at the top of each content file.
This metadata helps Pelican know what to do with each file, and help it differentiate between types of content so that each can be rendered correctly.

For blog posts, Pelican requires:

* **category** - for blogposts, should always the literal value `solr/blogposts`
* **Title** - a user-facing title for your post, to appear in RSS and at the top of your post.  May contain spaces, etc.
* **slug** - a unique identifier for your page, meant to be unique across all pages on `solr.apache.org`.  Often used in `save_as` and `URL` properties (see below).
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

### Previewing your Work

With the proper formatting in place your post _should_ be ready to appear on the blog, but it's worth checking locally to catch any potential issues before putting it in front of others for review.

Luckily, `solr-site` makes it easy to validate changes by building a local version of the Solr website.
You go to the root directory of the `solr-site` repository and run `./build.sh -l`.
This invokes Pelican to build the website, and spins up a web server (on port `8000`) to make the pages available.

You type `http://localhost:8000/blog.html` in your browser of choice and see your post in the list of recent posts on the landing page.

![Graph Query Blog Post Preview]({static}/images/blog/graph-query-blog-preview.png)

Clicking on the article link, you're taken to the page for your post.
It's gorgeous - there are a few Markdown syntax errors, but the "graph"-based puns in your content really pop!
Pelican detects your changes as soon as you fix the Markdown issues and rebuilds the site automatically, allowing you to see your fixes with just a "Refresh" in the browser.

You decide it's time to propose your post for review and publishing!

### Publishing - Creating your PR

TODO - git add, git commit, git push, create PR, conclusion
