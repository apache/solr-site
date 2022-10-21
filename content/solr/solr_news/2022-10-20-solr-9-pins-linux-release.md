Title: Solr Docker images now pin the Linux release
category: solr/news
save_as:

Solr 9 was released on May 12th, using the `eclipse-temurin:17-jre` base image. This image is pinned to the Java 17 and will
cause Solr 9 to always use an updated Java 17 release (if you pull the docker image from time to time that is).

However, our base image `17-jre` was not pinned to a specific Ubuntu Linux release. At the time of [Solr 9 release](http://localhost:8000/news.html#apache-solrtm-900-available) on May 12th
it would pull Ubuntu 20.04 (Focal Fossa), but at the end of May, it was [auto upgraded](https://github.com/docker-library/official-images/commit/6d689db4846a3eb4c2ebd0e5d06139c650ef3bbb) to the brand new Ubuntu
22.04 (Jammy Jellyfish). This was not our desire, and we have learnt that due to this, our image is no longer compatible
with Docker client versions before 20.10.16. Having a "floating" linux version can also break the image in other subtle
ways as well as images using Solr official image as base.

We therefore decided to start pinning not only Java release, but also Linux release in our official Docker images.
This means that Solr 9.0 will once again be based on Ubuntu 20.04. It will still receive important Linux bug fixes by 
re-pulling the image. When we upgrade to Ubuntu 22.04 in the futre, it will be a deliberate decision and not by accident.
