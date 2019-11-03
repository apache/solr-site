Title: Apache Lucene 4.8 will require Java 7
category: core/news
URL: 
save_as: 

The Apache Lucene committers decided with a large majority on the vote to require **Java 7** for the next minor release of Apache Lucene (version 4.8)!

The next release will also contain some improvements for Java 7:

* Better file handling (especially on Windows) in the directory implementations. Files can now be deleted on windows, although the index is still open - like it was always possible on Unix environments (delete on last close semantics).

* Speed improvements in sorting comparators: Sorting now uses Java 7's own comparators for integer and long sorts, which are highly optimized by the Hotspot VM.

If you want to stay up-to-date with Lucene and Solr, you should upgrade your infrastructure to Java 7.
Please be aware that you must use at least use Java 7u1.
The recommended version at the moment is Java 7u25. Later versions like 7u40, 7u45,... have a bug causing index corrumption.
Ideally use the Java 7u60 prerelease, which has fixed this bug. Once 7u60 is out, this will be the recommended version.
In addition, there is no more Oracle/BEA JRockit available for Java 7, use the official Oracle Java 7.
JRockit was never working correctly with Lucene/Solr (causing index corrumption), so this should not be an issue.
Please also review our list of JVM bugs: <http://wiki.apache.org/lucene-java/JavaBugs>

*EDIT (as of 15 April 2014):* The recently released Java 7u55 fixes the above bug causing index corrumption.
This version is now the recommended version for running Apache Lucene.

