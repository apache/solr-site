Title: Solr Downloads
URL: solr/downloads.html
save_as: solr/downloads.html
template: solr/downloads

Official releases are usually created when the [developers]({filename}/pages/whoweare.md)
feel there are sufficient changes, improvements and bug fixes to warrant a release.
Due to the voluntary nature of Solr, no releases are scheduled in advance.

#### Apache Solr 8.8.0 update
Solr 8.8.0 has been reported to have back-compat issues with SolrJ. 

Client applications that use a SolrJ version prior to 8.8.0 may experience a NullPointerException in ZkCoreNodeProps when requesting cluster state from Zookeeper. Upgrading your application to use SolrJ 8.8.0 will fix the issue.

This back compat break has been fixed in 8.8.1
