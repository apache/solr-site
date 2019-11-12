# Web site for Apache Lucene and Solr

## Building the site

### Installing Pelican

This site uses [Pelican][1] for static html generation. Pelican requires
Python 2.7.x and 3.5+ and can be installed with pip.

```sh
pip install pelican
```

The above is the simplest method, but the recommended approach is to create a
virtual environment for Pelican via virtualenv before installing Pelican. See
the [Pelican installation page][2] for more details.

```sh
virtualenv ~/virtualenvs/pelican
cd ~/virtualenvs/pelican
source bin/activate
```

### Additional Python Dependencies
Additional dependencies for Markdown and Pelican plugins are in requirements.txt.

```
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
both auto-regenerate and serve the output at http://localhost:8000:

```sh
pelican --autoreload --listen
```

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
