Title: A Search Hackathon at Community over Code, Glasgow 2026
category: solr/blogposts
summary: It’s always a pleasure to spend time with search people - and last month’s Community over Code, run by the Apache Foundation in Glasgow, was a great opportunity to do so. Here's what we worked on. Written by Charlie Hull, The Search Juggler.
slug: a-search-hackathon-at-coc-2026
URL: blogposts/a-search-hackathon-at-coc-2026.html
save_as: blogposts/a-search-hackathon-at-coc-2026.html

# A Search Hackathon at Community over Code, Glasgow 2026

It’s always a pleasure to spend time with search people - and last month’s [Community over Code](https://communityovercode.apache.org/events/glasgow-2026/), run by the Apache Foundation in Glasgow, was a great opportunity to do so. Although you might think that the majority of these people would be concerned with [Apache Solr](https://solr.apache.org/), the underlying [Apache Lucene](https://lucene.apache.org/) project underpins many other search engines including Elasticsearch and OpenSearch - so this was a gathering of search enthusiasts from many different backgrounds, companies and traditions.
On Monday I was pleased to join and help organise the Search Hackathon. 

For many, this was the first time they had met in person for a while (we were going to make up for this over a few evenings enjoying the attractions of Glasgow!). There were a lot of friendships renewed and sometimes begun between those who had already collaborated on a project but hadn’t yet met in person. This felt like a gathering that hadn’t happened since the old days of Lucene Revolution conferences, with around 20-30 people in the room, many of them Lucene and/or Solr committers - a chance to set the direction and make the big decisions about projects that underpin most of today’s search and AI infrastructure.

## What we worked on

We tried to record some of the work that was done - this isn’t in any particular order or an exhaustive list, as some people worked on their own or moved between projects, and apologies to anyone we missed out. I’ve added JIRA numbers and links to repositories where appropriate.

 * **David Smiley** - worked on highlighting in streaming expressions: two PRs, both addressing old JIRAs, [SOLR-3479](https://issues.apache.org/jira/browse/SOLR-3479) & [SOLR-9957](https://issues.apache.org/jira/browse/SOLR-9957)

 * **Alan Woodward, Luca Cavanna, Chris Hegarty, Mike Sokolov, Mike Drob, David Smiley, Uwe Schindler** - Played with lots of ideas for Lucene 11.  We started with a brainstorm on things that a major version bump and new JDK requirement allows us to do, including:
Merge RandomAccessInput interface into IndexInput: most implementations already extend both and it would remove a bunch of nasty instanceof checks and casting everywhere
Start using MemorySegment in public APIs, reducing the amount of data copying we have to do and simplifying things like off-heap memory access/direct IO.
We then talked about possible deprecations (this one was lots of fun…).  We ended up opening [an issue](https://github.com/apache/lucene/issues/16820) to discuss future removals of SpanQuery, ValueSource, FastVectorHighlighter and the majority of the query parsers

 * **Jan Høydahl & Andrey Ukhanov** - Grafana Dashboard in Solr 10. Revived a stale old JIRA/PR, [SOLR-18147](https://github.com/apache/lucene/issues/18147), split it in four consumable/reviewable parts. Jan implemented the first tooling focused part in [SOLR-18533](https://github.com/apache/lucene/issues/18533) ready for review. Andrey plans to iterate on the dashboard layout itself in [SOLR-18534](https://github.com/apache/lucene/issues/18543). Then the remaining parts are alert rules ([SOLR-18535](https://github.com/apache/lucene/issues/18535)) and OTEL push metrics ([SOLR-18536](https://github.com/apache/lucene/issues/18536)). 

 * **Prithvi S** - making Solr's Admin UI work across nodes. Added a node picker to Solr's Admin UI, allowing Thread Dump, Java Properties, Logging, Cores, and Dashboard screens to target any live node using the existing nodes= proxy. Also reorganised the sidebar into Cluster and Node sections, keeping the node-specific navigation out of the way when running Solr in standalone mode. Solr pull request
See [https://github.com/apache/solr/pull/5110]([https://github.com/apache/lucene/issues/16820](https://github.com/apache/solr/pull/5110)

 * **Andrzej Białecki** - worked on the [Solr MCP](https://github.com/apache/solr-mcp/) developer setup, tweaking the MCP built-in prompts

 * **Aditya Parikh** - Helped couple people including Andrej Bialecki and a graduate student from the University of Glasgow (new to Apache!) get set up and try out Solr-MCP in stdio & http modes by following [these steps](https://adityamparikh.github.io/solr-mcp/). They configured Claude Code, MCP inspector clients to use the Docker image of the MCP server, indexed sample data and executed searches against Solr running locally via Docker. They also visualized metrics and traces exported to a locally running LGTM container, an all in one observability platform, using a Grafana dashboard. 

 * **Eric Pugh** - Built [a Claude prompt](https://claude.ai/code/artifact/60d11ce1-18c8-4699-a3fd-cd2a3c19d8e3?sk=XTELG6l6Mk2QHBBDmdaDog) that categorizes PR’s by their impact.  Leaned into the movie Pacific Rim to gamify this work, and produced a Breach Report that demonstrates for a recent contributor the impact of their 59 different PRs - from small Category 1 to massive Category 5!  https://claude.ai/code/artifact/60d11ce1-18c8-4699-a3fd-cd2a3c19d8e3?sk=XTELG6l6Mk2QHBBDmdaDog
Then worked with Mike Drob to build a prompt that evaluates a PR and if it’s a bug (versus feature) oriented PR, then exercises the potential bug fix in order to reduce the amount of evaluation work that a committer has to perform to accept and merge the bug report.  [Example here](https://claude.ai/code/artifact/e5aa97fa-a8e5-476b-9897-b969602f3af4?sk=3E_BFM-yzYD2OEWy7ou4yQ) for a real submitted PR.

 * **Alec Bernardi** - I/O benchmarks for vector search. Added three layers of microbenchmarks for vector search in the Lucene [benchmark-jmh](https://github.com/apache/lucene/tree/main/lucene/benchmark-jmh) module:
    Directory reads
    Vector reads
    Vector bulk reads
  By comparing op/s, page faults, read amplification, and other results from these tests, we can figure out how close Lucene can drive I/O to device limits in cold/mixed index scenarios: particularly when performing vector queries using quantization with rescoring. PR incoming!

 * **Luke Kot** - [Lucene Monitor](https://lucene.apache.org/core/10_5_0/monitor/org/apache/lucene/monitor/package-summary.html) with negative queries. Made a sloppy PoC to show that it can improve performance. Iterating on minimizing the blast radius of the change. Chatted with Alan Woodward about the future of Lucene Monitor extensibility.

 * **Naveet** - Move vector graphs from heap to off heap. I added an opt-in way for Lucene to build merged HNSW graphs in native memory instead of on the Java heap, using a new offHeapGraphBuild option on the HNSW vector formats that leaves the index format unchanged.
    Benchmarks: On 1M 1024-dimension float32 vectors with a 1 GB heap, building the graph off-heap kept live heap flat at 91 MB during the force merge. The baseline used 375 MB at the median, 998 MB at p90, and peaked at the full 1 GB. The off-heap run also had no full GCs and much shorter pauses: 0.02 s in total with a longest pause of 1.7 ms, versus 0.52 s and 81.7 ms.
    Indexing speed, merge times, recall (0.951 vs 0.952), search latency and index size were essentially unchanged. Off-heap merges ran 2–3% faster, within noise for a single run.
    PR: [https://github.com/apache/lucene/pull/16815](https://github.com/apache/lucene/pull/16815) 

 * **Pukit Gupta** (Pulkitg64) - Subtract deleted vectors when recomputing the merge centroid. (PR: [#16819](https://github.com/apache/lucene/pull/16819)) This avoids scanning all vectors while calculating centroid for quantization during segment merging when there are deletes in the segment. Before this change, when there are deleted docs in a segment, we go over all live docs and calculate the mean of the vectors. Now after this change we are just going over deleted docs (if they are less than 50%) and deleting the vectors from the old centroid values. This should save some CPU in theory. 

 * **Shubham Chaudhary** - Reviewed some PRs related to the Lucene 11 feature ( [https://github.com/apache/lucene/pull/16812](https://github.com/apache/lucene/pull/16812) and [https://github.com/apache/lucene/pull/16795](https://github.com/apache/lucene/pull/16795) - WIP). Also, tried an optimization for [https://github.com/apache/lucene/issues/15778](https://github.com/apache/lucene/pull/15778) and checking if it choosing a bad entry point worsens the visited count or latency with choosing different params (less beamwidth, max-connections etc) but didn’t observe much of a slowdown. Though the idea seems a no-harm (next would be to open a PR to make top layer as exhaustive search since that will not increase the % of visited nodes more than 1%)

Thanks to everyone who came and for all the hard, collaborative work! It was fantastic to see such progress in only one day - although no doubt the work will continue. We need these kind of gatherings to swap ideas, build real-world relationships and to figure out the future. 

During the conference I had some interesting discussions about when we might all meet up next…watch this space for more news!

Charlie Hull\
[The Search Juggler](https://www.thesearchjuggler.com)
