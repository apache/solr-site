Title: Solr Alias Request Routing: Diagnosing a Query Coordination Hotspot
category: solr/blogposts
summary: Investigating a SolrCloud query coordination bottleneck involving collection aliases and distributing query coordination across search nodes. Written by Innovent Solutions.
slug: solr-alias-request-routing-query-coordination-hotspot
URL: blogposts/solr-alias-request-routing-query-coordination-hotspot.html
save_as: blogposts/solr-alias-request-routing-query-coordination-hotspot.html

# Solr Alias Request Routing: Diagnosing a Query Coordination Hotspot

In a production SolrCloud environment, distributing incoming search requests across nodes does not necessarily distribute query coordination evenly. While investigating a performance bottleneck involving collection aliases, Innovent Solutions identified how query coordination was becoming concentrated on a subset of nodes and developed an approach to distribute that work more evenly without changing the application's search endpoint.

Read the technical investigation in [Solr Alias Request Routing: Diagnosing a Query Coordination Hotspot](https://www.innoventsolutions.com/search-technology/solr-alias-request-routing-query-coordination-hotspot/).