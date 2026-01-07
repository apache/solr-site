# SPDX-License-Identifier: Apache-2.0
import json
import os
import sys

from cyclonedx.model.bom import Bom
from packageurl import PackageURL
from github import Auth, Github

from check_vex import should_generate_vex

BATCH_SIZE = 100

class Advisory:
    def __init__(self, cve_id: str, purl: PackageURL):
        self.cve_id = cve_id
        self.purl = purl

    def to_json(self):
        return {
            "cve_id": self.cve_id,
            "purl": self.purl.to_string()
        }


def get_github_client() -> Github:
    """
    Create and return a GitHub client using the GITHUB_TOKEN environment variable.
    """
    github_token = os.environ.get("GH_TOKEN")
    if not github_token:
        raise RuntimeError("GH_TOKEN environment variable is not set")
    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    return g


def get_advisories_by_purl(purls: list[PackageURL], g: Github) -> list[Advisory]:
    """
    Given a PackageURL, return a list of associated CVE IDs.
    """
    package_to_purl = {f"{p.namespace}:{p.name}": p for p in purls}
    affected = [f"{p.namespace}:{p.name}@{p.version}" for p in purls]
    advisories: list[Advisory] = []
    for gh_advisory in g.get_global_advisories(ecosystem="maven", affects=affected):
        for gh_vulnerability in gh_advisory.vulnerabilities:
            purl = package_to_purl.get(gh_vulnerability.package.name, None)
            if purl:
                advisories.append(Advisory(cve_id=gh_advisory.cve_id, purl=purl))
    return advisories


def get_purls(sbom: Bom) -> list[PackageURL]:
    """
    Extract PackageURLs from the SBOM components.
    """
    purls: list[PackageURL] = []
    for comp in sbom.components:
        if hasattr(comp, "purl"):
            purls.append(comp.purl)
    return purls


def list_advisories(sbom: Bom) -> list[Advisory]:
    """
    Generate a list of CVE IDs from the given SBOM file.
    """
    purls = get_purls(sbom)
    g = get_github_client()

    advisories: list[Advisory] = []
    for i in range(0, len(purls), BATCH_SIZE):
        batch = purls[i:i + BATCH_SIZE]
        advisories.extend(get_advisories_by_purl(batch, g))

    # Return unique advisories sorted by cve_id
    result = sorted({adv.cve_id: adv for adv in advisories}.values(), key=lambda a: a.cve_id)
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <sbom-path>", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(sys.argv[1]):
        print(f"SBOM file {sys.argv[1]} does not exist", file=sys.stderr)
        sys.exit(1)

    sbom_file = sys.argv[1]
    with open(sbom_file, "rb") as f:
        data = f.read()

    gh_repo = os.environ.get("GITHUB_REPOSITORY")
    if not gh_repo:
        print("GITHUB_REPOSITORY environment variable is not set", file=sys.stderr)
        sys.exit(1)
    sbom: Bom = Bom.from_json(data=json.loads(data))
    advisories = list_advisories(sbom)
    for advisory in advisories:
        cve_id = advisory.cve_id
        if should_generate_vex(gh_repo, cve_id) == 0:
            # Inputs for the generate_vex workflow
            inputs = {
                "sbom_file": sbom_file,
                "artifact_purl": advisory.purl.to_string(),
                "cve_id": cve_id
            }
            print(json.dumps(inputs))
