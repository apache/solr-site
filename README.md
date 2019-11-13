# Web site for Apache Lucene and Solr

This repository contains the "source code" of the Lucene/Solr website at [lucene.apache.org](https://lucene.apache.org/).

## Building the site

The site is written in Markdown syntax and built into a static site using [Pelican][1]. The site is re-built automatically by ASF Buildbot on every push to master branch and the result can be previewed at <TBD>. If the preview looks good, simply merge the change to branch <TBD> and the site will be deployed.

For larger edits it is recommended to build and preview the site locally. This is much faster. THe next sections detail that procedure.

### Installing Pelican

This site uses [Pelican][1] for static html generation. Pelican requires [Python 3.5+][4] and can be installed with pip. Assuming that you have python3 installed, simply run:

```sh
pip3 install -r requirements.txt
```

If you run into conflicts with existing packages, a solution is to use a virtual Python environment. See the [Pelican installation page][2] for more details. These are quick commands, Linux flavor:

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Generating HTML

Once Pelican is installed you can convert your content into HTML via the pelican
command (`content` is the default location to build from).

```sh
pelican
```

The above command will generate your site and save it in the `output/` using the
lucene theme and settings defined in `pelicanconf.py`

You can also tell Pelican to watch for your modifications, instead of manually
re-running it every time you want to see your changes. To enable this, run the
pelican command with the -r or --autoreload option. On non-Windows environments,
this option can also be combined with the -l or --listen option to simultaneously
both auto-regenerate and serve the output through a builtin webserver.

```sh
pelican --autoreload --listen
```

Now go to http://localhost:8000 to view the beautiful Lucene web page :)

## Bump Lucene/Solr latest version after a release

There are variables in **pelicanconf.py** to modify the latest 2 supported release
versions. This will affect all references to release version in the theme, but
not in pages or articles. Pelican views pages and articles as static write-once,
like a blog post, whereas the theme can be more dynamic and change with every
build.

Modify `LUCENE_LATEST_RELEASE` and `LUCENE_PREVIOUS_MAJOR_RELEASE`, and
`LUCENE_LATEST_RELEASE_DATE` to affect

* Full patch release versions in html such as "6.3.0".
* Minor release versions in html such as "6.3.x".
* References to unsupported versions such as "<6" in [Solr downloads][3].
* References to upcoming unreleased versions such as "7" in [Solr downloads][3]
  which is a +1 increment of the `LUCENE_LATEST_RELEASE` setting.
* Links to source, javadocs, PGP, and SHA512 which use underscores to separate
  version parts such as `6_3_0`
* References to the release date of the latest version which can be dynamically
  formatted for different pages.

[1]: https://blog.getpelican.com/
[2]: https://docs.getpelican.com/en/stable/install.html
[3]: https://lucene.apache.org/solr/downloads.html#about-versions-and-support
[4]: https://www.python.org/downloads/