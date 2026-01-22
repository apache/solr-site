# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
from pelican.contents import Content
from typing import Any
from functools import total_ordering


@total_ordering
class Version:
    """
    Version class to handle affected versions in metadata.
    """

    def __init__(self, major: int, minor: int, patch: int = 0,
                 pre_release: str = None):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.pre_release = pre_release

    def __lt__(self, other: Version | str) -> bool:
        """
        Compare two Version objects.
        """
        if isinstance(other, str):
            other = parse_version(other)
        if self.major != other.major:
            return self.major < other.major
        if self.minor != other.minor:
            return self.minor < other.minor
        if self.patch != other.patch:
            return self.patch < other.patch
        if self.pre_release != other.pre_release:
            if self.pre_release is None:
                return False
            if other.pre_release is None:
                return True
            return self.pre_release < other.pre_release
        return False

    def __eq__(self, other: Version | str) -> bool:
        """
        Check if two Version objects are equal.
        """
        if isinstance(other, str):
            other = parse_version(other)
        return (self.major == other.major and
                self.minor == other.minor and
                self.patch == other.patch and
                self.pre_release == other.pre_release)

    def __str__(self):
        """
        String representation of the Version object.
        """
        version_str = f"{self.major}.{self.minor}.{self.patch}"
        if self.pre_release:
            return f"{version_str}-{self.pre_release}"
        return version_str


def parse_version(version_str: str) -> Version:
    """
    Parse a version string into a Version object.
    """
    version, pre_release = version_str.split('-') if '-' in version_str else (version_str, None)
    parts = version.split('.')
    major = int(parts[0])
    minor = int(parts[1]) if len(parts) > 1 else 0
    patch = int(parts[2]) if len(parts) > 2 else 0
    return Version(major, minor, patch, pre_release)


class VersionRange:
    """
    VersionRange class to handle a range of versions, with inclusive/exclusive end.
    """

    def __init__(self, start: Version | None, end: Version, end_inclusive: bool = True):
        self.start = start
        self.end = end
        self.end_inclusive = end_inclusive

    def __str__(self):
        """
        String representation of the VersionRange object.
        """
        left = "[" if self.start is not None else "(-∞"
        right = "]" if self.end_inclusive else ")"
        if self.start != self.end or not self.end_inclusive:
            return f"{left}{self.start}, {self.end}{right}"
        return str(self.start)


class AffectedArtifact:
    def __init__(self, name: str, versions: list[VersionRange]):
        self.name = name
        self.versions = versions

    def __str__(self):
        """
        String representation of the AffectedArtifact object.
        """
        versions_str = ' ∪ '.join(str(vr) for vr in self.versions)
        return f"AffectedArtifact[name = {self.name}, versions = {versions_str}]"


def enrich_content_metadata(content: Content) -> None:
    """
    Enrich content metadata.

    This function parses the metadata for the vulnerable and impacted components,
    and replaces them with enriched AffectedArtifact objects.
    """
    metadata = content.metadata
    if 'vulnerable_component' in metadata:
        metadata['vulnerable_component'] = enrich_affected_artifact(metadata['vulnerable_component'])
        if 'impacted_component' in metadata:
            metadata['impacted_component'] = enrich_affected_artifact(metadata['impacted_component'])
        else:
            metadata['impacted_component'] = metadata['vulnerable_component']


def enrich_affected_artifact(content: Any) -> AffectedArtifact:
    """
    Parse the content to create an AffectedArtifact object.
    """
    name = content.get('name', 'Unknown Artifact')
    versions = [
        VersionRange(
            parse_version(v['introduced']) if 'introduced' in v else None,
            parse_version(v['fixed' if 'fixed' in v else 'last_affected']),
            v.get('last_affected', False)
        )
        for v in content.get('versions', [])
    ]
    return AffectedArtifact(name, versions)
