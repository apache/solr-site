package path;
use ASF::Value;
 
# taken  from django's url.py
$localMode = 0;  

# Patterns should go from more restrictive matches to less restrictive.
our @patterns = (

  [qr!core\/index\.mdtext$!, main => {
    template => "core.html",
    preprocess => 1,
    jira     => ASF::Value::Jira->new(limit => 5,
                                      url => "http://s.apache.org/corejira", localMode => $localMode),
    coreuser => ASF::Value::Mail->new(list => 'java-user@lucene.apache.org',
                                          limit => 3,
                                          localMode => $localMode),
    dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                          limit => 3, localMode => $localMode),

                                      }],  
  [qr!pylucene/jcc/index\.mdtext$!, main => { template => "jcc.html" }],
  [qr!pylucene/index\.mdtext$!, main => { template => "pylucene.html",
                                          preprocess => 1 }],
  [qr!openrelevance\/index\.mdtext$!, main => { template => "openrelevance.html",
                                                preprocess => 1 }],

  [qr!privacy\.mdtext$!, main => { template => "simple.html" }],
  [qr!core\/.*?\.mdtext$!, main => { template => "core-simple.html" }],

  [qr!solr\/index\.mdtext$!, main => {
    template => "solr-index.html",
    preprocess => 1,
    jira     => ASF::Value::Jira->new(limit => 5,
                                      url => "http://s.apache.org/solrjira",
                                      localMode => $localMode),
    solruser => ASF::Value::Mail->new(list => 'solr-user@lucene.apache.org',
                                          limit => 3, localMode => $localMode),
    dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                          limit => 3, localMode => $localMode),
    #solrtwitter  => ASF::Value::Twitter->new(search => '#solr', limit => 3,
    #                                    localMode => $localMode),
  }],
  [qr!solr\/features\.mdtext$!, main => {
    preprocess => 1,
    template => "solr-full-width.html"}],
  [qr!solr\/resources\.mdtext$!, main => {
    preprocess => 1,
    template => "solr-resources.html"}],
  [qr!solr\/community\.mdtext$!, main => {
    preprocess => 1,
    template => "solr-community.html"}],
  [qr!solr\/logos-and-assets\.mdtext$!, main => {
    preprocess => 1,
    template => "solr-full-width.html"}],
  [qr!solr\/downloads.mdtext$!, main => { 
    preprocess => 1, 
    template => "solr-page.html" } ],
  [qr@solr\/(?!index).*?\.mdtext$@, main => { template => "solr-page.html"}],

  [qr!pylucene/jcc/.*?\.mdtext$!, main => { template => "jcc-simple.html" }],
  [qr!pylucene/.*?\.mdtext$!, main => { template => "pylucene-simple.html" }],
  [qr!openrelevance\/.*?\.mdtext$!, main => { template => "openrelevance-simple.html" }],

	# keep the general one last
  [qr!\/index\.mdtext$!, main => { template => "main.html",
    preprocess => 1,
    coreuser => ASF::Value::Mail->new(list => 'java-user@lucene.apache.org',
                                          limit => 3,
                                          localMode => $localMode),
    dev => ASF::Value::Mail->new(list => 'dev@lucene.apache.org',
                                          limit => 3, localMode => $localMode),
    solruser => ASF::Value::Mail->new(list => 'solr-user@lucene.apache.org',
                                          limit => 3, localMode => $localMode),

  }],
  [qr!\.mdtext$!, main => { template => "simple.html"	 }],
) ;

# for specifying interdependencies between files - needs to be kept in sync w/ includes

our %dependencies = (
    "/core/index.mdtext" => [qw!/core/features.mdtext!],
    "/index.mdtext"      => [qw!/mainnews.mdtext!],
    "/solr/resources.mdtext"  =>  [qw!/latestversion.mdtext!],
    "/openrelevance/index.mdtext" => [qw!/openrelevance/orpnews.mdtext!],
    "/pylucene/index.mdtext"      => [qw!/pylucene/pynews.mdtext!],
);

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


