package path;
use ASF::Value;

# taken from django's url.py

# Patterns should go from more restrictive matches to less restrictive.
our @patterns = (
[qr!core\/index\.mdtext$!, main => { template => "core.html"	}],
	[qr!solr\/index\.mdtext$!, main => { template => "solr.html"
	 }],
	[qr!pylucene\/index\.mdtext$!, main => { template => "pylucene.html" }],
	[qr!openrelevance\/index\.mdtext$!, main => { template => "openrelevance.html" }],

	[qr!privacy\.mdtext$!, main => { template => "simple.html" }],

	  [qr!\/lucene\/index\.mdtext$!, main => { template => "main.html" }],

	 [qr!core\/.*?\.mdtext$!, main => { template => "core-simple.html"
	}],

	[qr!solr\/.*?\.mdtext$!, main => { template => "solr-simple.html"
	 }],
	[qr!pylucene\/.*?\.mdtext$!, main => { template => "pylucene-simple.html" }],
	[qr!openrelevance\/.*?\.mdtext$!, main => { template => "openrelevance-simple.html" }],

	# keep the general one last
  [qr!lucene\/index\.mdtext$!, main => { template => "main.html"}],
  [qr!\.mdtext$!, main => { template => "simple.html"	 }],
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


