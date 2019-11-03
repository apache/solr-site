Title: Apache Solr 5.5.0 and Reference Guide for 5.5 Available
category: solr/news
URL: 
save_as: 

The Lucene PMC is pleased to announce the release of Apache Solr 5.5.0

Solr is the popular, blazing fast, open source NoSQL search platform
from the Apache Lucene project. Its major features include powerful
full-text search, hit highlighting, faceted search, dynamic
clustering, database integration, rich document (e.g., Word, PDF)
handling, and geospatial search. Solr is highly scalable, providing
fault tolerant distributed search and indexing, and powers the search
and navigation features of many of the world's largest internet sites.

Solr 5.5.0 is available for immediate download at:
<http://lucene.apache.org/solr/mirrors-solr-latest-redir.html>

See the [CHANGES.txt](/solr/5_5_0/changes/Changes.html)
file included with the release for a full list of details.

This is expected to be the last 5.x feature release before Solr 6.0.

Release Highlights:

* The schema version has been increased to 1.6, and Solr now returns non-stored doc values fields along with stored fields

* The PERSIST CoreAdmin action has been removed

* The mergePolicy element is deprecated in favor of a similar mergePolicyFactory element, in solrconfig.xml

* CheckIndex now works on HdfsDirectory

* RuleBasedAuthorizationPlugin now allows wildcards in the role, and accepts an 'all' permission

* Users can now choose compression mode in SchemaCodecFactory

* Solr now supports Lucene's XMLQueryParser

* Collections APIs now have async support

* Uninverted field faceting is re-enabled, for higher performance on rarely changing indices

Also available is the Solr Reference Guide for Solr 5.5. This PDF serves as the definitive user's manual for Solr 5.5. It can be downloaded from the Apache mirror network: <https://s.apache.org/Solr-Ref-Guide-PDF>

