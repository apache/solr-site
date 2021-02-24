Title: Apache Lucene/Solr development moves to GIT
category: solr/news
URL: 
save_as: 

As of January 23rd 2016, Lucene/Solr source code is hosted in Apache's GIT repository.
This means that the old SVN repository is now stale and should not be used.
For information on working with git, please consult
[the Solr web site](https://solr.apache.org/resources.html#solr-version-control)
and the [wiki](https://wiki.apache.org/solr/Git%20commit%20process).

The [GitHub mirror](https://github.com/apache/lucene-solr/) remains at
the same location as before, but the contents have changed. We now have
one unified repo preserving the full history of both Lucene and Solr.
If you had a GitHub fork, you will find
that it has changed its "forked from" location, and any Pull Request will go to
that other fork instead of to the Lucene developers. The only known solution is to
delete your existing fork and re-fork from [GitHub](https://github.com/apache/lucene-solr/).

If you had active code changes and Pull Requests against our old GitHub mirror,
please see [the wiki](https://cwiki.apache.org/confluence/display/solr/HowToContribute#Working_with_GitHub)
for some suggestions on how to proceed.

The PMC is happy to answer any question you may have regarding this change.

