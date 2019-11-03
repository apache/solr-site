Title: Recommendation to update Apache POI in Apache Solr 4.8.0, 4.8.1, and 4.9.0 installations
category: news
URL: 
save_as: 

Apache Solr versions 4.8.0, 4.8.1, 4.9.0 bundle Apache POI 3.10-beta2 with its binary release tarball.
This version (and all previous ones) of Apache POI are vulnerable to the following issues:
CVE-2014-3529 *(XML External Entity (XXE) problem in Apache POI's OpenXML parser)*,
CVE-2014-3574 *(XML Entity Expansion (XEE) problem in Apache POI's OpenXML parser)*.

The Apache POI PMC released a bugfix version (3.10.1) today.

Solr users are affected by these issues, if they enable the "Apache Solr Content Extraction Library (Solr Cell)"
contrib module from the folder "contrib/extraction" of the release tarball.

Users of Apache Solr are strongly advised to keep the module disabled if they don't use it.
Alternatively, users of Apache Solr 4.8.0, 4.8.1, or 4.9.0 can update the affected libraries by
replacing the vulnerable JAR files in the distribution folder. Users of previous versions have
to update their Solr release first, patching older versions is impossible.

For detailed instructions, see [Solr's News](/solr/solrnews.html#18-august-2014-recommendation-to-update-apache-poi-in-apache-solr-480-481-and-490-installations)

