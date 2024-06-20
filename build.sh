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

# Using https://hub.docker.com/r/qwe1/docker-pelican as pelican image, supports both AMD64 and ARM64
PELICAN_IMAGE="qwe1/docker-pelican:4.8.0"
DOCKER_CMD="docker run --rm -w /work -p 8000:8000 -v $(pwd):/work $PELICAN_IMAGE"
unset SERVE
PIP_CMD="pip3 install -r requirements.txt"
PELICAN_CMD="pelican content -o output"
export SITEURL="https://solr.apache.org/"

function usage {
   echo "Usage: ./build.sh [-l] [<other pelican arguments>]"
   echo "       -l     Live build and reload source changes on localhost:8000"
   echo "       --help Show full help for options that Pelican accepts"
}

if ! docker -v >/dev/null 2>&1
then
  echo "ERROR: This script requires docker."
  echo "       Please install Docker and try again."
  echo
  usage
  exit 2
fi

if [[ ! -z $1 ]]; then
  if [[ "$1" == "-l" ]]; then
    SERVE=true
    shift
  else
    usage
    if [[ "$1" == "-h" ]]; then
      exit 0
    elif [[ "$1" == "--help" ]]; then
      echo
      echo "Below is a list of other arguments you can use which will be passed to pelican."
      echo
      $DOCKER_CMD pelican -h
      exit 0
    fi
  fi
fi
if [[ $SERVE ]]; then
  echo "Building Solr site locally. Goto http://localhost:8000 to view."
  echo "Edits you do to the source tree will be compiled immediately!"
  echo "$DOCKER_CMD $PIP_CMD; $PELICAN_CMD --autoreload --listen -b 0.0.0.0"
  $DOCKER_CMD $PIP_CMD; $PELICAN_CMD --autoreload --listen -b 0.0.0.0 $@
else
  echo "Building Solr site."
  echo "To build and serve live edits locally, run this script with -l argument. Use -h for help."
  $DOCKER_CMD $PIP_CMD; $PELICAN_CMD $@
fi
