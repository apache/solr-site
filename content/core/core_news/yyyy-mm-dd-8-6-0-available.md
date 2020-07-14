Title: Apache Lucene™ 8.6.0 available
category: core/news
URL:
save_as:

The Lucene PMC is pleased to announce the release of Apache Lucene 8.6.0.

Apache Lucene is a high-performance, full-featured text search engine library written entirely in Java. It is a technology suitable for nearly any application that requires full-text search, especially cross-platform.

This release contains numerous bug fixes, optimizations, and improvements, some of which are highlighted below. The release is available for immediate download at:

  <https://lucene.apache.org/core/downloads.html>

### Lucene 8.6.0 Release Highlights:

 * API change in: SimpleFSDireectory, IndexWriterConfig, MergeScheduler, SortFields, SimpleBindings, QueryVisitor, DocValues, CodecUtil.
 * New: IndexWriter merge-on-commit feature to selectively merge small segments on commit, subject to a configurable timeout, to improve search performance by reducing the number of small segments for searching.
 * New: Grouping by range based on DoubleValueSource and LongValueSource.
 * Optimizations: BKD trees and index, DoubleValuesSource/QueryValueSource, UsageTrackingQueryingCachingPolicy, FST, Geometry queries, Points, UniformSplit.
 * Others: Ukrainian analyzer, checksums verification, resource leaks fixes.

Please read CHANGES.txt for a full list of new features and changes:

  <https://lucene.apache.org/core/8_6_0/changes/Changes.html>