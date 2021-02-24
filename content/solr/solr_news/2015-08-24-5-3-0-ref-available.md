Title: Apache Solr 5.3.0 and Reference Guide for 5.3 available
category: solr/news
URL: 
save_as: 

Solr is the popular, blazing fast, open source NoSQL search platform
from the Apache Lucene project. Its major features include powerful
full-text search, hit highlighting, faceted search, dynamic
clustering, database integration, rich document (e.g., Word, PDF)
handling, and geospatial search.  Solr is highly scalable, providing
fault tolerant distributed search and indexing, and powers the search
and navigation features of many of the world's largest internet sites.

Solr 5.3.0 is available for immediate download at:
<https://solr.apache.org/downloads.html>

Solr 5.3 Release Highlights:

 * In addition to many other improvements in the security framework, Solr now includes an AuthenticationPlugin implementing HTTP Basic Auth that stores credentials securely in ZooKeeper. This is a simple way to require a username and password for anyone accessing Solr’s admin screen or APIs.
 * In built AuthorizationPlugin that provides fine grained control over implementing ACLs for various resources with permisssion rules which are stored in ZooKeeper.
 * The JSON Facet API can now change the domain for facet commands, essentially doing a block join and moving from parents to children, or children to parents before calculating the facet data.
 * Major improvements in performance of the new Facet Module / JSON Facet API.
 * Query and Range Facets under Pivot Facets. Just like the JSON Facet API, pivot facets can how nest other facet types such as range and query facets.
 * More Like This Query Parser options. The MoreLikeThis QParser now supports all options provided by the MLT Handler. The query parser is much more versatile than the handler as it works in cloud mode as well as anywhere a normal query can be specified.
 * Added Schema API support in SolrJ
 * Added Scoring mode for query-time join and block join.
 * Added Smile response format

See the [CHANGES.txt](/solr/5_3_0/changes/Changes.html) file included with the release for a full list of details.

Please report any feedback to the [mailing lists](https://solr.apache.org/discussion.html)

