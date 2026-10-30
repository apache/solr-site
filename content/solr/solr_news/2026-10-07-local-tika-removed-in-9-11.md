Title: Heads-up: the 'local' Tika extraction backend is gone in Solr 9.11
category: solr/news
save_as:

Solr normally keeps strict backwards compatibility within a major version. Solr 9.11.0 makes one exception: the embedded "local" Tika extraction backend has been removed from the extraction module (Solr Cell).

That backend was tied to Tika 1.28, which has been end-of-life since September 2022. Rather than keep shipping known vulnerabilities in a 9.x release, we removed it. The same removal is in Solr 10.0 and later, where it was part of the normal major-version deprecation cycle.

**Who is affected:** only users of `ExtractingRequestHandler` (`/update/extract`) with the local backend. If you don't use the extraction module, you can upgrade with no action.

**What to do:** run a [Tika Server](https://tika.apache.org/download.html) and point Solr at it:

```xml
<requestHandler name="/update/extract"
                class="solr.extraction.ExtractingRequestHandler">
  <str name="tikaserver.url">http://your-tika-server:9998</str>
</requestHandler>
```

The `parseContext.config` option is gone as well; Tika parser-specific properties are now configured on the Tika Server itself.

The reference guide has the full picture, including every `tikaserver.*` parameter and a Docker example:

  * [Indexing with Tika](https://solr.apache.org/guide/solr/9_11/indexing-guide/indexing-with-tika.html)
  * [Upgrade notes: Removing 'local' Tika](https://solr.apache.org/guide/solr/9_11/upgrade-notes/major-changes-in-solr-9.html#removing-local-tika)
  * [SOLR-18037](https://issues.apache.org/jira/browse/SOLR-18037)

We don't take a compatibility break in a minor release lightly, but shipping a known-vulnerable Tika 1.x was the worse option. Running Tika out of process also gives better isolation and resource control for extraction workloads.
