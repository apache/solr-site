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
  if [[ "$1" == "-l" ]]; then
    SERVE=true
    shift
  else
    echo "Usage: ./build.sh [-l] [<other pelican arguments>]"
    echo "       -l     Live build and reload source changes on localhost:8000"
    echo "       --help Show full help for options that Pelican accepts"
    if [[ "$1" == "-h" ]]; then
      exit 0
    elif [[ "$1" == "--help" ]]; then
      echo
      echo "Below is a list of other arguments you can use which will be passed to pelican."
      echo
      pelican --help
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
  source env/bin/activate && pip -q install --upgrade pip && pip -q install -r requirements.txt >/dev/null
fi
if [[ ! $(pelican -h 2>/dev/null) ]]; then
  echo "No pelican installed, attempting install"
  python3 -m venv env && source env/bin/activate && pip -q install --upgrade pip && pip install -r requirements.txt
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
  echo "To build and serve live edits locally, run this script with -l argument. Use -h for help."
  pelican $@
fi