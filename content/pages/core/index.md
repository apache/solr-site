Title: Apache Lucene Core
URL: core/index.html
save_as: core/index.html
theme: lucene-core
template: lucene/core/page

Apache Lucene<span style="vertical-align: super; font-size: xx-small">TM</span> is a
high-performance, full-featured text search engine library written entirely in Java.
It is a technology suitable for nearly any application that requires full-text search,
especially cross-platform.

Apache Lucene is an open source project available for free download. Please use the
links on the right to access Lucene.

# Lucene<span style="vertical-align: super; font-size: xx-small">TM</span> Features

Lucene offers powerful features through a simple API:


## Scalable, High-Performance Indexing

- over [150GB/hour on modern hardware][1]
- small RAM requirements -- only 1MB heap
- incremental indexing as fast as batch indexing
- index size roughly 20-30% the size of text indexed

## Powerful, Accurate and Efficient Search Algorithms

- ranked searching -- best results returned first
- many powerful query types: phrase queries, wildcard queries, proximity
  queries, range queries and more
- fielded searching (e.g. title, author, contents)
- sorting by any field
- multiple-index searching with merged results
- allows simultaneous update and searching
- flexible faceting, highlighting, joins and result grouping
- fast, memory-efficient and typo-tolerant suggesters
- pluggable ranking models, including the [Vector Space Model][2] and [Okapi BM25][3]
- configurable storage engine (codecs)


## Cross-Platform Solution

- Available as Open Source software under the [Apache License][4] which lets you use
  Lucene in both commercial and Open Source programs
- 100%-pure Java
- Implementations [in other programming languages available][5] that are index-compatible

[1]: http://home.apache.org/~mikemccand/lucenebench/indexing.html
[2]: http://en.wikipedia.org/wiki/Vector_Space_Model
[3]: http://en.wikipedia.org/wiki/Okapi_BM25
[4]: http://www.apache.org/licenses/LICENSE-2.0.html
[5]: https://cwiki.apache.org/confluence/display/lucene/LuceneImplementations
