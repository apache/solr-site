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

if [[ ! -z $1 ]]; then
  if [[ "$1" == "-s" ]]; then
    SERVE=true
    shift
  else
    echo "Usage: ./build.sh [-s] [<other pelican arguments>]"
    echo "       -s  Serve the site on localhost:8000 and auto reload on changes"
    if [[ "$1" == "-h" ]]; then
      exit 0
    fi
  fi
fi
if [[ ! $(python3 -h 2>/dev/null) ]]; then
  echo "No python installed"
  echo "Try one of"
  echo "  brew install python3"
  echo "  apt install python3"
  exit 2
fi
if [[ -d env ]]; then
  source env/bin/activate
fi
if [[ ! $(pelican -h 2>/dev/null) ]]; then
  echo "No pelican installed, attempting install"
  python3 -m venv env && source env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
  if [[ $? -gt 0 ]]; then
    echo "Failed pelican install, exiting."
    exit 2
  else
    echo "Install OK" && echo && echo
  fi
fi
if [[ $SERVE ]]; then
  echo "Building Lucene site locally. Goto http://localhost:8000 to view."
  echo "Edits you do to the source tree will be compiled immediately!"
  pelican --autoreload --listen $@
else
  echo "Building Lucene site."
  echo "To build and serve live edits locally, run this script with -s option."
  pelican $@
fi