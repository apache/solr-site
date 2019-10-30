Title: Updating the Lucene Website
URL:
save_as: site-instructions.html
template: lucene-tlp/page

## Editing Content on the Lucene<span style="vertical-align: super; font-size: xx-small">TM</span> sites

Editing any of the Lucene sites (Core, Solr<span style="vertical-align: super; font-size: xx-small">TM</span>, PyLucene) is easily done using the [ASF CMS](http://www.apache.org/dev/cms.html).

### Quick Edits

The easiest way to make quick edits to content on the website is using the [CMS Bookmarklet](https://cms.apache.org/#bookmark) to edit/stage/publish page edits.

### Major Edits

To get started, take the following steps from the command line:

* svn co https://svn.apache.org/repos/asf/lucene/cms/trunk cms/trunk
* svn co https://svn.apache.org/repos/infra/websites/cms/build if you wish to build and test locally
    * [http://www.apache.org/dev/cmsref.html#local-build](http://www.apache.org/dev/cmsref.html#local-build) for details on building locally.  If you are on a mac, you may need some perl dependencies installed.
    * cd asf-cms
    * ./build_site.pl --target-base=<path to output on local HTTPd server, I use ~/Sites> --source=../trunk/
* Edit the files in cms/trunk/content and cms/trunk/templates as you see fit.  When you are satisfied, svn commit.
* Browse to the [staging site](http://lucene.staging.apache.org/) to see them live (it may take a few seconds to build, you can track builds at [http://ci.apache.org/builders/lucene-site-staging](http://ci.apache.org/builders/lucene-site-staging)).

## Publishing Content to the Live Site
* Browse to [https://cms.apache.org/lucene/publish](https://cms.apache.org/lucene/publish) and log in.
* Confirm svn differences.
* Click the 'submit' button to publish changes.

## References

* [Markdown Reference](http://daringfireball.net/projects/markdown/syntax)

* [ASF CMS Reference](http://www.apache.org/dev/cmsref.html) and [ASF CMS](http://www.apache.org/dev/cms.html)
