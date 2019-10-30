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
command.

```sh
pelican content
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

[1]: https://blog.getpelican.com/
[2]: https://docs.getpelican.com/en/stable/install.html
