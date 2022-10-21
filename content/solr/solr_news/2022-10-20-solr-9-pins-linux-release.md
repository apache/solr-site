Title: Solr Docker images now pin the Linux release
category: solr/news
save_as:

Solr 9 was released on May 12th, using the `eclipse-temurin:17-jre` base image. Thus, we are pinned to Java 17 and Solr's
Docker image will thus always use an updated Java 17 version. If you pull the docker image from time to time that is.

However, the base image tag `17-jre` did not give us pinning to a specific Ubuntu Linux major release. 
At the time of [Solr 9 release](http://localhost:8000/news.html#apache-solrtm-900-available) on May 12th
it would pull Ubuntu 20.04 (Focal Fossa), but at the end of May, it was [auto upgraded](https://github.com/docker-library/official-images/commit/6d689db4846a3eb4c2ebd0e5d06139c650ef3bbb) to the brand new Ubuntu
22.04 (Jammy Jellyfish). This was not our desire, and we have learnt that due to this, our image is no longer compatible
with Docker client versions before 20.10.16. Having a "floating" linux release like this can also break the image in 
other subtle, ways as well as breaking images using Solr official image as base.

We therefore decided to start pinning not only Java release, but also Linux release in our official Docker images.
This means that Solr 9.0 is once again based on Ubuntu 20.04 Focal, i.e. a downgrade.

Note that our images will still receive important Linux bug fixes from time to time, but you won't get them unless you
re-pull the image. When we upgrade to Ubuntu 22.04 in the future, it will be a deliberate decision and not by accident.
