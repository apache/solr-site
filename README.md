# Website for Apache Solr

This repository contains the "source code" of the Solr website at [solr.apache.org](https://solr.apache.org/).

## Building the site

The site is written in [Markdown][9] syntax and built into a static site using [Pelican][1].

On each Pull Request we do a simple pelican build. The staging site is re-built automatically by Github Actions on every push to `main` branch, and the result can be previewed at [solr.staged.apache.org][6]. Build success/failure emails are sent to [commits@solr.apache.org][7] mailing list.
 
If the staged site looks good, simply merge the changes to branch `production` and the site will be deployed in a minute or two. Note that simple edits can also be done directly in the GitHub UI rather than clone -> edit -> commit -> push.

> **IMPORTANT**: Please never commit directly to `production` branch. All commits should go to `main, and then merge `main` to `production`. Note that it **is** possible to make a Pull Request for the merge from `main-->production`. If you do so, please merge using a merge commit rather than a squash merge.

For larger edits it is recommended to build and preview the site locally. This lets you see the result of your changes instantly without committing anything.
The bundled script uses a pelican docker image to build and serve the site locally. Please make sure you have docker installed.

    # Usage: ./build.sh [-l] [<other pelican arguments>]
    #        -l     Live build and reload source changes on localhost:8000
    #        --help Show full help for options that Pelican accepts
    ./build.sh -l

Now go to <http://localhost:8000> to view the beautiful Solr web page served from your laptop with live-preview of updates :)

### Other options

If you want to build the site without the docker image, you can install Python 3 and Pelican, see [manual install](./manual-install.md) for details.

On Windows, you can use the Windows Subsystem for Linux (WSL) to run the build script. Or you can run the docker command directly in a Terminal:

    docker run --rm -w /work -p 8000:8000 -v $(pwd):/work qwe1/docker-pelican:4.8.0 pip3 install -r requirements.txt; pelican content -r -l -b 0.0.0.0

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
[6]: https://solr.staged.apache.org
[7]: https://lists.apache.org/list.html?commits@solr.apache.org
[9]: http://daringfireball.net/projects/markdown/syntax
 
