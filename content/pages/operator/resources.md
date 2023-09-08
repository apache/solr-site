Title: Resources
URL: operator/resources.html
save_as: operator/resources.html
template: operator/resources

All resources are currently found in the [Solr Operator repository](https://github.com/apache/solr-operator), but will eventually be moved to the website.

## Tutorials ##

* [Solr Operator Quick Start](https://apache.github.io/solr-operator/docs/local_tutorial)  
  This is a basic tutorial designed for users new to Kubernetes and the Solr Operator
* [Exploring the Apache Solr Operator v0.3.0 on GKE]({filename}/pages/operator/articles/explore-v030-gke.md)  
  This is an advanced tutorial for users ready to use the Solr Operator for Solr Clouds running in a production environment.
* [Guide to Autoscaling Solr on Kubernetes](https://sematext.com/blog/solr-operator-autoscaling-tutorial/)  
  This is a tutorial designed to help users to setup a basic implementation of Autoscaling using the [HorizontalPodAutoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/).

Users who have completed the tutorial are encouraged to review the [other documentation available](#documentation).

***

## Helm Charts ##

If you want to run Solr on Kubernetes, the easiest way to get started is via installing the Helm charts below.

* **Solr Operator** - A management layer that runs independently in Kubernetes. Only deploy 1 per Kubernetes cluster or namespace.
* **Solr** - A SolrCloud cluster. In order to deploy this Helm chart successfully, you must first install the Solr Operator and Solr CRDs. Follow the instructions on the ArtifactHub page below.

<div style="display:flex; justify-content: space-evenly; flex-wrap: wrap">
  <div class="artifacthub-widget" data-url="https://artifacthub.io/packages/helm/apache-solr/solr-operator" data-theme="light" data-header="false" data-responsive="true" style="flex-basis:0"></div><script async src="https://artifacthub.io/artifacthub-widget.js"></script>
  <div class="artifacthub-widget" data-url="https://artifacthub.io/packages/helm/apache-solr/solr" data-theme="light" data-header="false" data-responsive="true" style="flex-basis:0"></div><script async src="https://artifacthub.io/artifacthub-widget.js"></script>
</div>

***

## Documentation ##

<h3 class="offset" id="the-apache-solr-reference-guide">The Apache Solr Reference Guide</h3>

Current documentation can be found in the [repo's github pages](https://apache.github.io/solr-operator/docs), soon it will be migrated to this site.

<h3 class="offset" id="additional-documentation">Additional Documentation</h3>

Additional documentation, including upgrade notes, can be found in the [Solr Operator's README](https://github.com/apache/solr-operator#solr-operator).

***

## Presentations and Videos ##

<!-- TODO: WOULD BE NICE TO HAVE A SLIDER OR RANDOMLY PICKED VIDEO HERE -->

<h3 class="offset" id="youtube">YouTube</h3>

[Introducing the Solr Operator - Activate 2019](https://youtu.be/MD6NXTrA3xo?si=_ALWWzxKgBWqiCjX)

[Demystifying the Solr Operator - Berlin Buzzwords 2021](https://youtu.be/zl22KyzWqtM?si=OdQKJYY6EnpQufXw)

[Using Solr unconventionally to serve 26bn+ documents - Berlin Buzzwords 2022](https://youtu.be/tr4XYE2r0dE?si=PZfUPMLHkDkFw_Ow)

[Rethinking Autoscaling for Apache Solr using Kubernetes - Berlin Buzzwords 2023](https://youtu.be/HfHa4Q4YaTU?si=cCiadyOmjlo86sVF)

<h3 class="offset" id="youtube">Conferences with Solr talks</h3>

[Videos from Past Activate / Lucene/Solr revolution events](https://www.activate-conf.com/more-events)

[Videos from past Berlin Buzzwords events](https://www.youtube.com/c/PlainSchwarzUG/playlists?view=50&sort=dd&shelf_id=1)

[Search YouTube for Solr](https://www.youtube.com/results?search_query=solr+operator)

If you have a Solr Operator video or presentationthat you would like to see listed here, please [edit this website and submit a Pull Request](/editing-website.html).

