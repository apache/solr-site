# SPDX-License-Identifier: Apache-2.0

import json
import urllib.request
import urllib.error

from typing import Any

# Base URL for callgraph metadata
CALLGRAPH_BASE_URL = "https://raw.githubusercontent.com/vex-generation-toolset/callgraph-metadata/refs/heads/main/"


def __get_root_cause_url(cve: str) -> str:
    cve_parts = cve.split("-", 3)
    if len(cve_parts) != 3 or cve_parts[0] != "CVE":
        raise ValueError(f"Invalid CVE identifier: {cve}")
    return f"{CALLGRAPH_BASE_URL}/vulnerabilities/{cve_parts[1]}/{cve_parts[2]}/root-cause.json"

def get_root_cause(cve: str) -> Any:
    cve_url = __get_root_cause_url(cve)

    try:
        with urllib.request.urlopen(cve_url, timeout=10) as resp:
            return json.load(resp)
    except urllib.error.URLError as e:
        raise RuntimeError(f"Failed to fetch CVE data from {cve_url}: {e}") from e

def find_root_cause_functions(cve: str) -> list[str]:
    """
    Given a CVE identifier, return a list of root cause functions associated with that CVE.
    """
    cve_data = get_root_cause(cve)
    root_cause_objects = cve_data.get("root_cause_functions", [])
    root_cause_functions = []
    for func in root_cause_objects:
        function_name = func.get("methods", [])
        root_cause_functions.extend(function_name)

    return root_cause_functions