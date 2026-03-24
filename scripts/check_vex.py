# SPDX-License-Identifier: Apache-2.0
import os.path
import sys

from github import Auth, Github
from github.PaginatedList import PaginatedList
from github.PullRequest import PullRequest
from root_cause import get_root_cause


def __has_root_cause(cve: str) -> bool:
    """
    Check if the given CVE has a root cause function defined.
    """
    try:
        get_root_cause(cve)
        return True
    except RuntimeError:
        return False


def __has_open_pull_request(repo: str, cve: str) -> bool:
    """
    Check if there is an open pull request for the given CVE.
    """
    github_token = os.environ.get("GH_TOKEN")
    if not github_token:
        raise RuntimeError("GH_TOKEN environment variable is not set")

    auth = Auth.Token(github_token)
    g = Github(auth=auth)
    pull_requests: PaginatedList[PullRequest] = g.get_repo(repo).get_pulls(state="open")
    for pr in pull_requests:
        if cve in pr.title:
            return True
    return False


def should_generate_vex(repo: str, cve: str) -> int:
    """
    Check if a VEX document for the given CVE should be generated.

    Args:
        repo: GitHub repository in the format "owner/repo"
        cve: CVE identifier

    Returns:
        0 if VEX document should be generated.
    """
    # If the VEX input file already exists, skip generation
    if os.path.exists(f"vex-input/{cve}.json"):
        return 1

    # If there is already an open PR for this CVE, skip generation
    if __has_open_pull_request(repo, cve):
        return 2

    # If there is no root cause defined for this CVE, skip generation
    if not __has_root_cause(cve):
        return 3

    return 0


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <github-repo> <cve-id>", file=sys.stderr)
        sys.exit(127)

    repo = sys.argv[1]
    cve = sys.argv[2]

    sys.exit(should_generate_vex(repo, cve))
