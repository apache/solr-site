package path;
use ASF::Value;

# taken from django's url.py

# Patterns should go from more restrictive matches to less restrictive.
our @patterns = (

  #	[qr!/sitemap\.html$!, sitemap => { headers => { title => "Lucene Sitemap" }} ],
  # separate ones for the index.html pages, as they will include the news
  #TODO: fix the duplication of SVN, jira, etc.

	 [qr!core\/index\.mdtext$!, main => { template => "core.html",
	   svn      => ASF::Value::SVN->new(project => "lucene/dev/trunk/lucene", limit => 5),
  	 jira     => ASF::Value::Jira->new(limit => 5,
                                url => "https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-comments-rss/temp/SearchRequest.xml?jqlQuery=project+%3D+LUCENE+ORDER+BY+updatedDate+DESC&tempMax=20"),
     dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                            limit => 3),
     coreuser => ASF::Value::Mail->new(list => 'java-user@lucene.apache.org',
                                            limit => 3)
	}],
	[qr!solr\/index\.mdtext$!, main => { template => "solr.html",
	  svn      => ASF::Value::SVN->new(project => "lucene/dev/trunk/solr", limit => 5),
  	 jira     => ASF::Value::Jira->new(limit => 5,
                                url => "https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-comments-rss/temp/SearchRequest.xml?jqlQuery=project+%3D+SOLR+ORDER+BY+updatedDate+DESC&tempMax=20"),
     dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                            limit => 3),
     solruser => ASF::Value::Mail->new(list => 'solr-user@lucene.apache.org',
                                            limit => 3),
	 }],
	[qr!pylucene\/index\.mdtext$!, main => { template => "pylucene.html" }],
	[qr!openrelevance\/index\.mdtext$!, main => { template => "openrelevance.html" }],

	[qr!privacy\.mdtext$!, main => { template => "simple.html",
	   svn      => ASF::Value::SVN->new(project => "lucene", limit => 5),
  	 jira     => ASF::Value::Jira->new(limit => 5,
                                url => "https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-comments-rss/temp/SearchRequest.xml?jqlQuery=project+%3D+LUCENE+ORDER+BY+updatedDate+DESC&tempMax=20"),
     dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                            limit => 3),
     coreuser => ASF::Value::Mail->new(list => 'java-user@lucene.apache.org',
                                            limit => 3)
	  }],
	 [qr!core\/.*?\.mdtext$!, main => { template => "core-simple.html",
	   svn      => ASF::Value::SVN->new(project => "lucene/dev/trunk/lucene", limit => 5),
  	 jira     => ASF::Value::Jira->new(limit => 5,
                                url => "https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-comments-rss/temp/SearchRequest.xml?jqlQuery=project+%3D+LUCENE+ORDER+BY+updatedDate+DESC&tempMax=20"),
     dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                            limit => 3),
     coreuser => ASF::Value::Mail->new(list => 'java-user@lucene.apache.org',
                                            limit => 3)
	}],
	[qr!solr\/.*?\.mdtext$!, main => { template => "solr-simple.html",
	  svn      => ASF::Value::SVN->new(project => "lucene/dev/trunk/solr", limit => 5),
  	 jira     => ASF::Value::Jira->new(limit => 5,
                                url => "https://issues.apache.org/jira/sr/jira.issueviews:searchrequest-comments-rss/temp/SearchRequest.xml?jqlQuery=project+%3D+SOLR+ORDER+BY+updatedDate+DESC&tempMax=20"),
     dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                            limit => 3),
     solruser => ASF::Value::Mail->new(list => 'solr-user@lucene.apache.org',
                                            limit => 3),
	 }],
	[qr!pylucene\/.*?\.mdtext$!, main => { template => "pylucene-simple.html" }],
	[qr!openrelevance\/.*?\.mdtext$!, main => { template => "openrelevance-simple.html" }],

	# keep the general one last
  [qr!lucene\/index\.mdtext$!, main => { template => "main.html",
     dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                            limit => 3),
     coreuser => ASF::Value::Mail->new(list => 'java-user@lucene.apache.org',
                                            limit => 3),
     solruser => ASF::Value::Mail->new(list => 'solr-user@lucene.apache.org',
                                            limit => 3),
	 }],
	 [qr!\.mdtext$!, main => { template => "simple.html",
     dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                            limit => 3),
     coreuser => ASF::Value::Mail->new(list => 'java-user@lucene.apache.org',
                                            limit => 3),
     solruser => ASF::Value::Mail->new(list => 'solr-user@lucene.apache.org',
                                            limit => 3),
	 }],
) ;

# for specifying interdependencies between files

#our %dependencies = (
#    "/lucene/sitemap.html" => [ grep s!^content!!, glob "content/lucene/*.mdtext" ],
#);

1;

=head1 LICENSE

           Licensed to the Apache Software Foundation (ASF) under one
           or more contributor license agreements.  See the NOTICE file
           distributed with this work for additional information
           regarding copyright ownership.  The ASF licenses this file
           to you under the Apache License, Version 2.0 (the
           "License"); you may not use this file except in compliance
           with the License.  You may obtain a copy of the License at

             http://www.apache.org/licenses/LICENSE-2.0

           Unless required by applicable law or agreed to in writing,
           software distributed under the License is distributed on an
           "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
           KIND, either express or implied.  See the License for the
           specific language governing permissions and limitations
           under the License.


