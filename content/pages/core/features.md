Title: Lucene<span style="vertical-align: super; font-size: xx-small">TM</span> Features
URL: core/features.html
save_as: core/features.html
template: lucene/core/page

Lucene offers powerful features through a simple API:

## Scalable, High-Performance Indexing

* over [150GB/hour on modern hardware](http://home.apache.org/~mikemccand/lucenebench/indexing.html)
* small RAM requirements -- only 1MB heap
* incremental indexing as fast as batch indexing
* index size roughly 20-30% the size of text indexed

## Powerful, Accurate and Efficient Search Algorithms

* ranked searching -- best results returned first
* many powerful query types: phrase queries, wildcard queries, proximity queries, range queries and more
* fielded searching (e.g. title, author, contents)
* sorting by any field
* multiple-index searching with merged results
* allows simultaneous update and searching
* flexible faceting, highlighting, joins and result grouping
* fast, memory-efficient and typo-tolerant suggesters
* pluggable ranking models, including the [Vector Space Model](http://en.wikipedia.org/wiki/Vector_Space_Model) and [Okapi BM25](http://en.wikipedia.org/wiki/Okapi_BM25)
* configurable storage engine (codecs)

## Cross-Platform Solution

* Available as Open Source software under the [Apache License](https://www.apache.org/licenses/LICENSE-2.0.html) which lets you use Lucene in both commercial and Open Source programs
* 100%-pure Java
* Implementations in [other programming languages available](https://cwiki.apache.org/confluence/display/lucene/LuceneImplementations) that are index-compatible