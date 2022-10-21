Title: Solr 8 on Docker changes to Eclipse Temurin JDK
category: solr/news
save_as:

The official docker image for Solr 8.11 has been running on [OpenJDK 11 JRE](https://hub.docker.com/_/openjdk). However due to that project discontinuing their Java 11 Docker images, and Solr 8.11 still being supported by the Apache Solr project, we needed to switch to another OpenJDK vendor. We chose [Eclipse Temurin](https://hub.docker.com/_/eclipse-temurin), the same vendor we use for our Solr 9 image.

Users should be aware that on your next `docker pull solr:8.11.2` you will be upgraded. For most users there will be no issues, as it is mainly a new distribution of the same upstream Java version. However, if you use our image as base image and rely on specific tools to be present, you may need to adapt. While `openjdk:11-jre` uses `Debian GNU/Linux 11 (bullseye)`, the `eclipse-temurin:11-jre` image uses `Ubuntu 22.04.1 LTS (Jammy Jellyfish)`.

Furthermore, there is now no difference between the `solr:11-jre` and `solr:11-jre-slim` images, because our new vendor only offers one variant which is fairly slim already. 
