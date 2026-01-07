#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0

import json
import os
import sys
import tempfile

from cyclonedx.model.bom import Bom
from packageurl import PackageURL

from typing import Any
from dependency_chain import find_dependency_chains
from root_cause import find_root_cause_functions
from vex_generation_service.analysis import Analysis

CALLGRAPH_BASE_URL = "https://raw.githubusercontent.com/vex-generation-toolset/callgraph-metadata/refs/heads/main"


def __vex_generation_request(sbom: Bom, artifact: PackageURL, cve_id: str) -> Any:
    root_cause_functions = find_root_cause_functions(cve_id)
    dependency_chains = find_dependency_chains(sbom, artifact)
    return {
        "cve_id": cve_id,
        "purl": artifact.to_string(),
        "root_cause_functions": root_cause_functions,
        "chains": [
            [{
                "purl": f"pkg:{purl.type}/{purl.namespace}/{purl.name}@{purl.version}",
                "callgraph": f"{CALLGRAPH_BASE_URL}/callgraphs/{purl.namespace}/{purl.name}/{purl.version}/callgraph.json"
            } for purl in chain] for chain in dependency_chains
        ],
        "vex": {}
    }


def generate_vex(sbom: Bom, artifact: PackageURL, cve_id: str, tempdir: str) -> Any:
    """
    Generate a VEX for the given SBOM, artifact, and CVE ID.

    Args:
        sbom: The CycloneDX SBOM.
        artifact: The PackageURL of the artifact to analyze.
        cve_id: The CVE identifier.

    Returns:
        The path to the generated JSON file.
    """
    request = __vex_generation_request(sbom, artifact, cve_id)
    vex_input = f"{tempdir}/vex-input.json"
    vex_output = f"{tempdir}/vex-output.json"
    try:
        with open(vex_input, "w") as f:
            json.dump(request, f)
            f.close()
        analysis = Analysis(vex_input)
        analysis.run()
        analysis.export_vex(vex_output)
        with (open(vex_output, "r") as f):
            vex_data = json.load(f)
        return vex_data
    finally:
        os.unlink(vex_input)
        os.unlink(vex_output)


def __format_chain(chain_data: list[Any]) -> str:
    purls = [PackageURL.from_string(vex_data["purl"]) for vex_data in chain_data]
    return " -> ".join([purl.name for purl in purls])


def __format_pull_request(cve_id: str, solr_version: str, vex_data: list[list[Any]]) -> str:
    result_lines = []
    result_lines.append(f"Analyse impact of {cve_id} on Solr {solr_version}\n")
    for chain_idx, chain_data in enumerate(vex_data):
        result_lines.append(f"# Chain {chain_idx + 1}: {__format_chain(chain_data)}\n")
        for artifact_idx, artifact_data in enumerate(chain_data):
            purl = PackageURL.from_string(artifact_data.get("purl", ""))
            analysis = artifact_data.get("vex", {}).get("vulnerabilities", [{}])[0].get("analysis", {})
            state = analysis.get("state", "unknown")
            result_lines.append(f"## Artifact: {purl.name} ({state})\n")
            message = (
                analysis.get("detail", {})
                .get("explanations", [{}])[0]
                .get("message", "")
            )
            result_lines.append(message)
    return "\n".join(result_lines)


def __get_temp_dir() -> str:
    tmpdir = os.environ.get("RUNNER_TEMP")
    return tmpdir if tmpdir else tempfile.gettempdir()


def __generate_vex_input_entry(vex_data: list[list[Any]], artifact_purl: PackageURL, solr_version: str) -> Any:
    entries = []
    for chain_data in vex_data:
        # The first entry is the one for Solr itself
        artifact_data = chain_data[0] if len(chain_data) > 0 else {}
        vulnerability = artifact_data.get("vex", {}).get("vulnerabilities", [{}])[0]
        cve_id = vulnerability["id"]
        state = vulnerability.get("analysis", {}).get("state")
        if state == "unaffected":
            state = "not_affected"
        summary = f"{cve_id} in {artifact_purl.name}@{artifact_purl.version} is {"NOT reachable" if state == "not_affected" else "REACHABLE"} in Apache Solr."
        entries.append({
            "ids": [vulnerability.get("id")],
            "versions": solr_version,
            "jars": [
                f"{artifact_purl.name}-{artifact_purl.version}.jar"
            ],
            "analysis": {
                "state": state,
                "detail": summary
            }
        })
    # Return the first entry for which the vulnerability is reachable
    for vex_input_entry in entries:
        state = vex_input_entry["analysis"]["state"]
        if state != "not_affected":
            return vex_input_entry
    return entries[0] if len(entries) > 0 else {}


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: generate_vex.py <sbom> <artifact_purl> <cve_id>")
        sys.exit(1)

    sbom_path = sys.argv[1]
    artifact_purl = sys.argv[2]
    cve_id = sys.argv[3]

    with open(sbom_path, "rb") as f:
        data = f.read()

    sbom: Bom = Bom.from_json(data=json.loads(data))
    solr_version = sbom.metadata.component.version
    artifact = PackageURL.from_string(artifact_purl)
    tempdir = __get_temp_dir()
    vex_data = generate_vex(sbom, artifact, cve_id, tempdir)
    # Write PR content to temporary file
    with open(f"{tempdir}/commit-message.md", "w") as pr_file:
        pr_file.write(__format_pull_request(cve_id, solr_version, vex_data))
    # Write original analysis output to vexplanation folder
    with open(f"vexplanation/{cve_id}.json", "w") as analysis_file:
        json.dump(vex_data, analysis_file, indent=2)
    # Write summarized VEX to vex-input folder
    with open(f"vex-input/{cve_id}.json", "w") as vex_input_file:
        json.dump(__generate_vex_input_entry(vex_data, artifact, solr_version), vex_input_file, indent=2)
