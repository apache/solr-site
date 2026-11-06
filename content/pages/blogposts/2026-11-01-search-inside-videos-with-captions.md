Title: Search Inside Your Videos: Indexing WebVTT Captions in Solr
category: solr/blogposts
summary: How to index WebVTT caption files in Solr so a search finds the exact second a phrase is spoken, including phrases that run across two caption cues. Written by Mark Santos.
slug: search-inside-videos-with-captions
URL: blogposts/search-inside-videos-with-captions.html
save_as: blogposts/search-inside-videos-with-captions.html

# Search Inside Your Videos: Indexing WebVTT Captions in Solr

Caption files make video searchable: every WebVTT cue pairs a line of speech with the time it is spoken. This article indexes each video as one Solr document holding its whole transcript, with each cue's character offset and start time stored beside it, so phrase queries still match when a phrase runs across two cues. The unified highlighter (with `hl.fragsize=0`) marks every match in the full transcript, and the stored offsets turn each mark into a timestamped link. It also covers the default `hl.maxAnalyzedChars` limit of 51,200 characters, past which a long transcript comes back with no highlight and so no timestamp. Tested with Solr 10.1.0.

The complete post can be read here: [How to Search Inside Your Videos: Caption Search with Apache Solr](https://www.markstudios.com/blog/search-inside-videos-solr-captions).
