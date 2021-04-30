# Website for Apache Solr

This repository contains the "source code" of the Solr website at [solr.apache.org](https://solr.apache.org/).

## Building the site

The site is written in [Markdown][9] syntax and built into a static site using [Pelican][1]. The site is re-built automatically by [ASF Buildbot][5] on every push to main branch, and the result can be previewed at [solr.staged.apache.org][6]. Build success/failure emails are sent to [commits@solr.apache.org][7] mailing list. Read more about the mechanics behind auto building in [INFRA Confluence][8].
 
If the staged site looks good, simply merge the changes to branch `production` and the site will be deployed in a minute or two. Note that simple edits can also be done directly in the GitHub UI rather than clone -> edit -> commit -> push.

> **IMPORTANT**: Please never commit directly to `production` branch. All commits should go to `main, and then merge `main` to `production`. Note that it **is** possible to make a Pull Request for the merge from `main-->production`. If you do so, please merge using a merge commit rather than a squash merge.

For larger edits it is recommended to build and preview the site locally. This lets you see the result of your changes instantly without committing anything. The next sections detail that procedure. The TL;DR instructions goes like this:

    # Usage: ./build.sh [-l] [<other pelican arguments>]
    #        -l     Live build and reload source changes on localhost:8000
    #        --help Show full help for options that Pelican accepts
    ./build.sh -l

Now go to <http://localhost:8000> to view the beautiful Solr web page served from your laptop with live-preview of updates :)

### Installing Pelican by hand

The site uses [Pelican][1] for static html generation. Pelican requires [Python 3.5+][4] and can be installed with pip.

**The `build.sh` script mentioned in the above paragraph takes care of setting up your Pelican environment,** and you can skip this part unless you want to understand the moving parts and install things by hand. Assuming that you have python3 installed, simply run:

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

## Updating site during a Solr release

The release manager documentation will contain detailed instructions on how to update the site during a release. Some of the boring version number update and download link generation is handled by Pelican, see below.

JavaDoc publishing and Solr RefGuide publishing is **not** done through this repo, but in SVN as detailed in Release Manager instructions, and will then appear in respective sections of the website automatically, see `.htaccess` for how.

### Bump Solr latest version after the release

There are variables in **pelicanconf.py** to modify the latest 2 supported release versions. This will affect all references to release version in the theme, but not in pages or articles. Pelican views pages and articles as static write-once, like a blog post, whereas the theme can be more dynamic and change with every build.

Modify `SOLR_LATEST_RELEASE` and `SOLR_PREVIOUS_MAJOR_RELEASE`, and
`SOLR_LATEST_RELEASE_DATE` to affect

* Full patch release versions in html such as "6.3.0".
* Minor release versions in html such as "6.3.x".
* References to unsupported versions such as "<6" in [Solr downloads][3].
* References to upcoming unreleased versions such as "7" in [Solr downloads][3]
  which is a +1 increment of the `SOLR_LATEST_RELEASE` setting.
* Links to source, javadocs, PGP, and SHA512 which use underscores to separate
  version parts such as `6_3_0`
* References to the release date of the latest version which can be dynamically
  formatted for different pages.

[1]: https://blog.getpelican.com/
[2]: https://docs.getpelican.com/en/stable/install.html
[3]: https://solr.apache.org/downloads.html#about-versions-and-support
[4]: https://www.python.org/downloads/
[5]: https://ci2.apache.org/#/builders/3
[6]: https://solr.staged.apache.org
[7]: https://lists.apache.org/list.html?commits@solr.apache.org
[8]: https://wiki.apache.org/confluence/display/INFRA/Git+-+.asf.yaml+features
[9]: http://daringfireball.net/projects/markdown/syntax
