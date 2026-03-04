# SPDX-License-Identifier: Apache-2.0

from packageurl import PackageURL
from cyclonedx.model.bom import Bom
from cyclonedx.model.bom_ref import BomRef
from cyclonedx.model.dependency import Dependency
from collections.abc import Iterable


class Chain:
    def __init__(self, artifact: PackageURL, callgraph_url: str):
        self.artifact = artifact
        self.callgraph_url = callgraph_url

    def to_json(self) -> dict[str, str]:
        return {
            "purl": self.artifact.to_string(),
            "callgraph": self.callgraph_url
        }


def __create_if_absent(dependencies_by_ref: dict[BomRef, Dependency], ref: BomRef) -> Dependency:
    dep = dependencies_by_ref.get(ref)
    if not dep:
        dep = Dependency(ref)
        dependencies_by_ref[ref] = dep
    return dep


def __reverse_graph(dependencies: Iterable[Dependency], root_ref: BomRef) -> Dependency:
    root = Dependency(root_ref)
    dependencies_by_ref: dict[BomRef, Dependency] = {root_ref: root}

    for dep in dependencies:
        parent = __create_if_absent(dependencies_by_ref, dep.ref)
        for child in dep.dependencies:
            # parent depends on child
            child_dep = __create_if_absent(dependencies_by_ref, child.ref)
            # Prevent cycles
            child_dep.dependencies.add(parent)

    return root


def __purls_by_ref(sbom: Bom) -> dict[BomRef, PackageURL]:
    chains: dict[BomRef, PackageURL] = {}
    for comp in sbom.components:
        purl = comp.purl
        if not purl:
            continue
        chains[comp.bom_ref] = purl
    return chains


def __find_dependency_chains(root: Dependency, purls_by_ref: dict[BomRef, PackageURL]) -> list[list[PackageURL]]:
    """
    Find all dependency chains from the root to leaf dependencies.
    """
    all_chains = []

    def dfs(current: Dependency, chain: list[PackageURL], visited: set[Dependency]):
        current_purl = purls_by_ref.get(current.ref)
        if current in visited:
            # There is a cycle; stop this branch (or handle differently)
            return

        visited.add(current)
        if current_purl:
            chain.append(current_purl)

        if len(current.dependencies) == 0:
            all_chains.append(chain[::-1])  # append a copy of the current path in reverse order
        else:
            for child in current.dependencies:
                dfs(child, chain, visited)

        # backtrack
        if current_purl:
            chain.pop()
        visited.remove(current)

    dfs(root, [], set())
    return all_chains


def find_dependency_chains(sbom: Bom, artifact_purl: PackageURL) -> list[list[PackageURL]]:
    """
    Generate a VEX generator request for the given artifact string.
    """
    bom_ref: BomRef | None = None
    for comp in sbom.components:
        if (comp.purl
                and comp.purl.namespace == artifact_purl.namespace
                and comp.purl.name == artifact_purl.name
                and comp.purl.version == artifact_purl.version):
            bom_ref = comp.bom_ref
            break

    if not bom_ref:
        raise ValueError(f"Artifact {artifact_purl} not found in SBOM components")

    root: Dependency = __reverse_graph(sbom.dependencies, bom_ref)
    purls_by_ref: dict[BomRef, PackageURL] = __purls_by_ref(sbom)
    return __find_dependency_chains(root, purls_by_ref)
