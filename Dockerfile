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

# Base image pinned by digest — updated automatically by Dependabot (docker ecosystem).
# When Dependabot opens a bump PR, also regenerate requirements.txt (see README.md).
FROM python:3.14-alpine@sha256:01f125438100bb6b5770c0b1349e5200b23ca0ae20a976b5bd8628457af607ae
WORKDIR /work
COPY requirements.txt .
RUN pip3 install --require-hashes -r requirements.txt && rm requirements.txt