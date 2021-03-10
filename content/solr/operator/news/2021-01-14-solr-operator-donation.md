Title: Solr Operator donated to Apache Solr
category: solr/operator/news
save_as:

The Apache Software Foundation's board today established Solr as a Top Level Project (TLP).
Solr has been a Lucene sub-project since its incubation in 2006, governed by the Lucene PMC,
and has since the 3.1 release also shared source code repository with Lucene.

### What's the background?

The change was proposed by members of the Lucene PMC, and a vote in June 2020 decided
that Solr would be a separate TLP. Later, the Lucene PMC decided that the Solr project
would be bootstrapped with the same set of committers and PMC members as the "mother" Lucene project.

### How does this affect users?

The Solr software will not change at all as a result of this, but users will see these changes:

1. Solr gets a new website at [solr.apache.org](http://solr.apache.org/)
2. Solr gets a new download location in the mirrors
3. The email address of the users mailing-list will change, but subscribers will be moved automatically

### How does this affect developers?

Developers will have to do a number of things to adapt to the change

1. Subscribe to the new mailing lists. See [Mailing Lists & Chat](/community.html#mailing-lists-chat) for instructions
2. Start using [the new git location](/community.html#version-control) by cloning or defining a new git remote
3. Realize that lucene will be a build dependency of Solr on the main branch (once the code migration is done)
4. Backported bug fixes for Solr 8.8 must be submitted to the Lucene git, for a joint bugfix release

**NOTE:** Some things may be in flux during the migration work.
