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

# Base image and packages are defined in Dockerfile (digest-pinned, tracked by Dependabot).
# To regenerate requirements.txt after changing requirements.in, see README.md#updating-the-dependency-lockfile
SOLR_LOCAL_PELICAN_IMAGE="solr-pelican-image"
DOCKER_CMD="docker run --rm -ti -w /work -p 8000:8000 -v $(pwd):/work $SOLR_LOCAL_PELICAN_IMAGE"
unset SERVE
unset BUILD
unset LOCK
PELICAN_CMD="pelican content -o output"
export SITEURL="https://solr.apache.org/"

# Option definitions: "short_flag:long_flag:description"
# Omit short_flag (leave empty before first colon) for long-only options.
# Usage text and getopt spec are both derived from this array.
OPTIONS=(
  "l:live:Live build and reload source changes on localhost:8000"
  "b:build:Force rebuild of the local Docker image"
  ":lock:Regenerate requirements.txt from requirements.in (use with -b to also rebuild image)"
  "h:help:Show this help message"
  ":pelican-help:Show all options accepted by Pelican"
)

function usage {
  echo "Usage: ./build.sh [OPTIONS] [-- <pelican arguments>]"
  echo ""
  echo "Options:"
  for opt_def in "${OPTIONS[@]}"; do
    short="${opt_def%%:*}"
    rest="${opt_def#*:}"
    long="${rest%%:*}"
    desc="${rest#*:}"
    if [[ -n "$short" ]]; then
      printf "  -%s, --%-16s %s\n" "$short" "$long" "$desc"
    else
      printf "      --%-16s %s\n" "$long" "$desc"
    fi
  done
  echo ""
  echo "Any extra arguments after -- are passed directly to Pelican."
}

# Build short and long getopt spec strings from OPTIONS array.
function _getopt_specs {
  local short="" long=""
  for opt_def in "${OPTIONS[@]}"; do
    s="${opt_def%%:*}"
    l="${opt_def#*:}"; l="${l%%:*}"
    [[ -n "$s" ]] && short+="$s"
    long+="${long:+,}${l}"
  done
  echo "${short}|${long}"
}

function build_image {
  echo "Building local Docker image for Pelican, called $SOLR_LOCAL_PELICAN_IMAGE."
  docker build --no-cache -t $SOLR_LOCAL_PELICAN_IMAGE .
}

function regen_lockfile {
  ensure_image
  echo "Regenerating requirements.txt from requirements.in inside Docker..."
  docker run --rm -w /work -v "$(pwd):/work" $SOLR_LOCAL_PELICAN_IMAGE \
    pip-compile --quiet --strip-extras --allow-unsafe --generate-hashes --output-file=requirements.txt requirements.in
  echo "requirements.txt updated."
}

function ensure_image {
  if ! docker inspect $SOLR_LOCAL_PELICAN_IMAGE >/dev/null 2>&1
  then
    build_image
  fi
}

function check_requirements_update {
  # Check requirements.txt — that is what is COPY'd into the Dockerfile
  local req_mod_time
  if [[ $(uname) == "Darwin" ]]; then
    req_mod_time=$(stat -f "%m" requirements.txt)
  else
    req_mod_time=$(stat -c "%Y" requirements.txt)
  fi

  # Get the build timestamp of the docker image
  local image_build_time
  image_build_time=$(docker inspect --format='{{.Created}}' $SOLR_LOCAL_PELICAN_IMAGE)

  # Parse the timestamp into seconds since epoch in UTC
  if [[ $(uname) == "Darwin" ]]; then
    # macOS date command workaround
    image_build_time=$(echo "$image_build_time" | awk -F '.' '{print $1}')
    image_build_time=$(date -ju -f "%Y-%m-%dT%H:%M:%S" "$image_build_time" "+%s")
  else
    # Linux date command
    image_build_time=$(date -d "$(echo "$image_build_time" | cut -d'.' -f1 | sed 's/T/ /; s/Z//')" --utc "+%s")
  fi

  # Compare the timestamps and rebuild if requirements.txt is newer than the image
  if [[ $req_mod_time -gt $image_build_time ]]; then
    echo "requirements.txt has been updated since the last build, rebuilding image!"
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

# Handle a single parsed option. Returns 1 (exit loop) on --.
function handle_opt {
  case "$1" in
    -l|--live)      SERVE=true ;;
    -b|--build)     BUILD=true ;;
    --lock)         LOCK=true ;;
    -h|--help)      usage; exit 0 ;;
    --pelican-help) ensure_image; $DOCKER_CMD pelican -h; exit 0 ;;
    --)             return 1 ;;
    *)              echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
}

# Use GNU getopt when available (detected via exit code 4 from getopt -T).
# GNU getopt gives proper error messages and handles --opt=value and option
# reordering. Falls back to a plain bash loop which handles all our flag options.
getopt -T &>/dev/null; _getopt_test=$?
if [[ $_getopt_test -eq 4 ]]; then
  specs=$(_getopt_specs)
  PARSED=$(getopt -o "${specs%%|*}" --long "${specs#*|}" -n "build.sh" -- "$@") || { usage; exit 1; }
  eval set -- "$PARSED"
  while true; do
    if handle_opt "$1"; then shift; else shift; break; fi
  done
else
  while [[ $# -gt 0 ]]; do
    if handle_opt "$1"; then shift; else shift; break; fi
  done
fi

if [[ $LOCK ]]; then
  regen_lockfile
  if [[ ! $BUILD ]]; then
    echo "Run './build.sh -b' to rebuild the Docker image with the updated lockfile."
    exit 0
  fi
fi

if [[ $BUILD ]]; then
  build_image
else
  ensure_image
  check_requirements_update
fi

if [[ $SERVE ]]; then
  echo "Building Solr site locally. Goto http://localhost:8000 to view."
  echo "Edits you do to the source tree will be compiled immediately!"
  $DOCKER_CMD sh -c "$PELICAN_CMD --autoreload --listen -b 0.0.0.0 $*"
else
  echo "Building Solr site locally."
  echo "To build and serve live edits locally, run this script with -l argument. Use -h for help."
  $DOCKER_CMD sh -c "$PELICAN_CMD $*"
fi
