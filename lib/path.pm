package path;
use ASF::Value;

# taken from django's url.py

our @patterns = (

    [qr!^/index\.html$!, news_page =>
      {
        svn      => ASF::Value::SVN->new(limit => 5),
        jira     => ASF::Value::Jira->new(limit => 5,
                                          url => "http://s.apache.org/q4"),
        announce => ASF::Value::Mail->new(list => 'announce@apache.org',
                                          limit => 5),
        planet   => ASF::Value::Blogs->new(blog => "planet", limit=> 5),
        blog     => ASF::Value::Blogs->new(blog => "foundation", limit=> 5),
        twitter  => ASF::Value::Twitter->new(name => 'TheASF', limit => 5),
      },
    ],

    [qr!^/dev/index\.html$!, news_page =>
      {
        svn      => ASF::Value::SVN->new(limit => 5),
        twitter  => ASF::Value::Twitter->new(name=>"infrabot", limit => 5),
        blog     => ASF::Value::Blogs->new(blog => "infra", limit=> 5),
        jira     => ASF::Value::Jira->new(limit => 5,
                                          url => "http://s.apache.org/lg"),
      },
    ],

    [qr!^/dev/sitemap\.html$!, sitemap => { headers => { title => "Developer Sitemap" }} ],

    [qr!^/licenses/exports/index\.html$!, exports => {} ],

    [qr!\.mdtext$!, single_narrative => { template => "single_narrative.html" }],
);


# for specifying interdependencies between files

our %dependencies = (
    "/dev/sitemap.html" => [ grep s!^content!!, glob "content/dev/*.mdtext" ],
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
