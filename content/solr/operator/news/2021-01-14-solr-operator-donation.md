Title: Solr Operator donated to Apache Solr
category: solr/operator/news
save_as:

The Apache Software Foundation's board today accepted Bloomberg's donation of the Solr Operator as a sub-project of the Apache Solr project.

### What's the background?

The Solr Operator is software that manages an environment to run Solr and related services on Kubernetes.
It was created and open sourced by [Bloomberg](https://www.techatbloomberg.com/) in early 2019.

### How does this affect users?

The Solr Operator repo is now maintained by the Apache Solr PMC, and lives at a new location:

1. The code base can now be found under the apache organization on Github, [apache/solr-operator](https://github.com/apache/solr-operator).
2. The Solr Operator has a section on the solr website gets a new website at [https://solr.apache.org/operator](https://solr.apache.org/operator)
3. The Solr Operator Docker image will now be available at [apache/solr-operator](https://hub.docker.com/r/apache/solr-operator).
   Old versions, released before the project was donated to Apache, can still be found at [bloomberg/solr-operator](https://hub.docker.com/r/bloomberg/solr-operator).
4. The Helm charts for installing the Solr Operator now live in the [Apache Solr helm repo](https://artifacthub.io/packages/helm/apache-solr/solr-operator).

### How does this affect developers?

Developers will not need to make many changes to their workflow.
Make sure to run the new `make prepare` command before submitting a PR and you should be good to go.
