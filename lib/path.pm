package path;
use ASF::Value;

# taken from django's url.py

our @patterns = (

#	[qr!/sitemap\.html$!, sitemap => { headers => { title => "Lucene Sitemap" }} ],
	[qr!core\/.*?\.mdtext$!, main => { template => "core.html"}],
	[qr!solr\/.*?\.mdtext$!, main => { template => "solr.html" }],
	[qr!pylucene\/.*?\.mdtext$!, main => { template => "pylucene.html" }],
	[qr!openrelevance\/.*?\.mdtext$!, main => { template => "orp.html" }],
	# keep the general one last
  [qr!\.mdtext$!, main => { template => "main.html",
     svn      => ASF::Value::SVN->new(project => "lucene", limit => 5),
  #	 jira     => ASF::Value::Jira->new(limit => 5,
  #                                          url => "https://issues.apache.org/jira/plugins/servlet/streams?key=LUCENE"),
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


