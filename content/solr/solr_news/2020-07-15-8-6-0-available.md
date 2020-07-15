Title: Apache Solr™ 8.6.0 available
category: solr/news
save_as:

The Lucene PMC is pleased to announce the release of Apache Solr 8.6.0.

Solr is the popular, blazing fast, open source NoSQL search platform from the Apache Lucene project. Its major features include powerful full-text search, hit highlighting, faceted search, dynamic clustering, database integration, rich document handling, and geospatial search. Solr is highly scalable, providing fault tolerant distributed search and indexing, and powers the search and navigation features of many of the world's largest internet sites.

Solr 8.6.0 is available for immediate download at:

  <https://lucene.apache.org/solr/downloads.html>

### Solr 8.6.0 Release Highlights:

 * Cross-Collection Join Queries: Join queries can now work cross-collection, even when shared or when spanning nodes.
 * Search: Performance improvement for some types of queries when using when exact hit count isn't needed by using BlockMax WAND algorithm.
 * Streaming Expression: Percentiles and standard deviation aggregations added to stats, facet and time series.  Streaming expressions added to /export handler.  Drill Streaming Expression for efficient and accurate high cardinality aggregation.
 * Package manager: Support for cluster (CoreContainer) level plugins.
 * Health Check: HealthCheckHandler can now require that all cores are healthy before returning OK.
 * Zookeeper read API: A read API at /api/cluster/zk/* to fetch raw ZK data and view contents of a ZK directory.
 * Admin UI: New panel with security info in admin UI's dashboard.
 * Query DSL: Support for {param:ref} and {bool: {excludeTags:""}}
 * Ref Guide: Major redesign of Solr's documentation.

Please read CHANGES.txt for a full list of new features and changes:

  <https://lucene.apache.org/solr/8_6_0/changes/Changes.html>

Solr 8.6.0 also includes features, optimizations  and bugfixes in the corresponding Apache Lucene release:

  <https://lucene.apache.org/core/8_6_0/changes/Changes.html>