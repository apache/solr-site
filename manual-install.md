# Installing Pelican by hand

The site uses [Pelican][1] for static html generation. Pelican requires [Python 3.5+][4] and can be installed with pip.

**The `build.sh` script mentioned in REAME is the easiest way of building the site**, and you can skip this part unless you want to understand the moving parts and install things by hand. 

## Install Python 3

First, you need to install Python 3. You can download the latest version from the [Python website][4] or
use your package manager to install it. For example, on macOS:

```shell
brew install python
```

## Install Pelican

To install pelican and requirements, simply run the following command in the root of the repository:

```sh
pip3 install -r requirements.txt
```

If you run into conflicts with existing packages, a solution is to use a virtual Python environment. See the [Pelican installation page][2] for more details. These are quick commands, Linux flavor:

```sh
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Once Pelican is installed you can convert your content into HTML via the pelican command (`content` is the default location to build from).

```sh
pelican
```

The above command will generate your site and save it in the `output/` folder using the solr theme and settings defined in `pelicanconf.py`

You can also tell Pelican to watch for your modifications, instead of manually re-running it every time you want to see your changes. To enable this, run the pelican command with the `-r` or `--autoreload` option. On non-Windows environments, this option can also be combined with the `-l` or `--listen` option to simultaneously both auto-regenerate and serve the output through a builtin webserver on <http://localhost:8000>.

```sh
pelican --autoreload --listen
```

Remember that on Mac/Linux you can use the `build.sh` script with `-l` option to do the same.

[1]: https://blog.getpelican.com/
[4]: https://www.python.org/downloads/
