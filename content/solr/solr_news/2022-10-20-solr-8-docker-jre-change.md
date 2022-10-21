Title: Solr 8 Docker image changes to Eclipse Temurin JDK
category: solr/news
save_as:

The official docker image for Solr 8.11 has been running on [Oracle OpenJDK 11 JRE](https://hub.docker.com/_/openjdk). However, due to Oracle's new release policies, they now no longer provide support for JDK11. Since Solr 8.11 is still being supported by the Apache Solr project, we needed to switch to another OpenJDK vendor with JDK11 support. We chose [Eclipse Temurin](https://hub.docker.com/_/eclipse-temurin) from the Adoptium project. This is the same vendor as we use for our Solr 9 image, and their [JDK11 support lasts until October 2024](https://adoptium.net/support/). 

Users should be aware that on your next `docker pull solr:8.11.2` you will be upgraded. For most users there will be no issues, as it is mainly a new distribution of the same upstream OpenJDK version. However, if you use our image as base image and rely on specific tools to be present, you may need to adapt. While `openjdk:11-jre` uses `Debian GNU/Linux 11 (bullseye)`, the `eclipse-temurin:11-jre-focal` image uses `Ubuntu 20.04.5 LTS (Focal Fossa)`.

Furthermore, there is now no difference between the `solr:11-jre` and `solr:11-jre-slim` images, because our new vendor only offers one variant which is fairly slim already.
