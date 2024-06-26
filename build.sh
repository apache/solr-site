#!/bin/bash
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Fail on error
set -e
#set -x

# Using https://hub.docker.com/r/qwe1/docker-pelican as pelican image, supports both AMD64 and ARM64
PELICAN_IMAGE="qwe1/docker-pelican:4.8.0"
SOLR_PELICAN_IMAGE="solr-pelican-image"
DOCKER_CMD="docker run --rm -ti -w /work -p 8000:8000 -v $(pwd):/work $SOLR_PELICAN_IMAGE"
unset SERVE
PIP_CMD="pip3 install -r requirements.txt"
PELICAN_CMD="pelican content -o output"
PELICAN_OPTS=""
export SITEURL="https://solr.apache.org/"

function usage {
   echo "Usage: ./build.sh [-l] [-b] [<other pelican arguments>]"
   echo "       -l     Live build and reload source changes on localhost:8000"
   echo "       -b     Re-build local docker image, re-installing packages from requirements.txt"
   echo "       --help Show full help for options that Pelican accepts"
}

function build_image {
  echo "Building local Docker image for Pelican, called $SOLR_PELICAN_IMAGE."
  # Make a new local image with the pip packages installed
  docker rm -f solr-pelican >/dev/null 2>&1 || true
  docker run --name solr-pelican -w /work -v $(pwd):/work $PELICAN_IMAGE sh -c "$PIP_CMD"
  docker commit solr-pelican $SOLR_PELICAN_IMAGE
  docker rm -f solr-pelican >/dev/null 2>&1 || true
}

function ensure_image {
  if ! docker inspect $SOLR_PELICAN_IMAGE >/dev/null 2>&1
  then
    build_image
  fi
}

if ! docker -v >/dev/null 2>&1
then
  echo "ERROR: This script requires docker."
  echo "       Please install Docker and try again."
  echo
  usage
  exit 2
fi

while getopts ":lbh-:" opt; do
  case ${opt} in
    l )
      SERVE=true
      ;;
    b )
      build_image
      ;;
    h )
      usage
      exit 0
      ;;
    - )
      case "${OPTARG}" in
        help )
          echo
          echo "Below is a list of other arguments you can use which will be passed to pelican."
          echo
          $DOCKER_CMD pelican -h
          exit 0
          ;;
        * )
          PELICAN_OPTS+="--${OPTARG} "
          ;;
      esac
      ;;
    \? )
      PELICAN_OPTS+="-${OPTARG} "
      ;;
  esac
done
shift $((OPTIND -1))

ensure_image
if [[ $SERVE ]]; then
  echo "Building Solr site locally. Goto http://localhost:8000 to view."
  echo "Edits you do to the source tree will be compiled immediately!"
  echo "Changes to requirements.txt will require using -b option to rebuild the image."
  $DOCKER_CMD sh -c "$PELICAN_CMD --autoreload --listen -b 0.0.0.0 $PELICAN_OPTS $*"
else
  echo "Building Solr site locally."
  echo "To build and serve live edits locally, run this script with -l argument. Use -h for help."
  echo "Changes to requirements.txt will require using -b option to rebuild the image."
  $DOCKER_CMD sh -c "$PELICAN_CMD $PELICAN_OPTS $*"
fi
