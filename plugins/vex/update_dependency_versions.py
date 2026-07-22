#!/usr/bin/env python3
"""Regenerate solr-dependency-versions.json from a real syft SBOM scan of each
tracked Solr release's actual binary distribution, instead of resolving a
declared Maven dependency graph. A declared graph misses anything Solr bundles
at packaging time (e.g. its own Jetty server) and can conflate a tracked
artifact with an unrelated same-named dependency pulled in by some other,
optional module -- syft instead reads the real jars on disk.

Usage:
    python3 plugins/vex/update_dependency_versions.py [VERSION ...]

With no arguments, every version in solr-versions.txt is (re)scanned, which
downloads and unpacks each release's full binary distribution (tens to a few
hundred MB each) -- expect a full run to take a long time and a lot of
bandwidth, since archive.apache.org (the only host with the complete release
history) serves archived releases slowly. Pass one or more specific versions
(e.g. just-released ones) to only refresh those, and/or --slim to scan the
much smaller "-slim" distribution (5-6x less data, 9.x+ only) at the cost of
missing dependencies that only live in optional modules (Hadoop, Tika, etc).

Only already-tracked dependencies (existing keys in solr-dependency-versions.json)
are touched, and only to fill in a missing (dependency, Solr version) entry --
an existing value is never overwritten. A resolved value that disagrees with
what's on file is reported as a conflict for a human to look into rather than
applied. Newly-seen third-party dependencies that aren't tracked yet are also
reported, for a human to decide whether to start tracking them.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

VEX_DIR = Path(__file__).resolve().parent
REPO_ROOT = VEX_DIR.parent.parent
VERSIONS_FILE = VEX_DIR / 'solr-versions.txt'
DEP_VERSIONS_FILE = VEX_DIR / 'solr-dependency-versions.json'
SYFT_IMAGE = 'anchore/syft:latest'

# First-party groups: never worth tracking as a "third-party dependency".
EXCLUDED_GROUPS = {'org.apache.solr', 'org.apache.lucene'}

# Candidate (base URL, filename) templates to try, in order, covering Solr's
# release-hosting history: the current standalone repo (9.0+), the older
# combined Lucene/Solr repo (~3.1-8.x), and that repo's older "apache-solr-"
# filename prefix (pre ~4.3-ish). The first template that downloads
# successfully is used.
URL_TEMPLATES = [
    'https://archive.apache.org/dist/solr/solr/{v}/solr-{v}.tgz',
    'https://archive.apache.org/dist/lucene/solr/{v}/solr-{v}.tgz',
    'https://archive.apache.org/dist/lucene/solr/{v}/apache-solr-{v}.tgz',
]

# The much smaller "-slim" distribution (9.x+ only) excludes optional modules
# (Hadoop, Tika/extraction, etc.), so any dependency that only lives in one of
# those won't be found this way -- it'll just stay whatever it already is.
SLIM_URL_TEMPLATES = [
    'https://archive.apache.org/dist/solr/solr/{v}/solr-{v}-slim.tgz',
]


def download_distribution(version, dest, slim=False):
    """Download the first resolvable release tarball for `version` into `dest`.
    Returns True on success, False if no URL template resolved."""
    templates = (SLIM_URL_TEMPLATES + URL_TEMPLATES) if slim else URL_TEMPLATES
    for template in templates:
        url = template.format(v=version)
        try:
            with urllib.request.urlopen(url, timeout=60) as resp, open(dest, 'wb') as out:
                shutil.copyfileobj(resp, out)
            return True
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            dest.unlink(missing_ok=True)
            continue
    return False


def run_syft(extracted_dir):
    """Run syft against the extracted distribution directory, returning the
    parsed CycloneDX JSON document, or None on failure."""
    try:
        result = subprocess.run(
            ['docker', 'run', '--rm', '-v', f'{extracted_dir}:/work',
             SYFT_IMAGE, '/work', '-o', 'cyclonedx-json'],
            capture_output=True, text=True, timeout=300,
        )
    except FileNotFoundError:
        sys.exit('ERROR: docker is required to run syft (see README.md for setup).')
    if result.returncode != 0 or not result.stdout.strip():
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


PURL_RE = re.compile(r'^pkg:maven/([^/]+)/([^@]+)@([^?]+)')


def iter_maven_packages(sbom):
    """Yield (group, artifact, version) for every Maven-purl component in a
    syft CycloneDX SBOM."""
    for component in sbom.get('components', []):
        m = PURL_RE.match(component.get('purl', ''))
        if m:
            yield m.groups()


def scan_version(version, work_dir, slim=False):
    """Download, extract, and syft-scan `version`'s binary distribution under
    `work_dir`. Returns the parsed CycloneDX SBOM, or None if the release
    couldn't be downloaded, extracted, or scanned."""
    tarball = work_dir / 'dist.tgz'
    if not download_distribution(version, tarball, slim=slim):
        print(f'  no release tarball found for {version}, skipping', file=sys.stderr)
        return None
    extract_dir = work_dir / 'extracted'
    extract_dir.mkdir()
    try:
        with tarfile.open(tarball) as tf:
            try:
                tf.extractall(extract_dir, filter='data')
            except TypeError:
                tf.extractall(extract_dir)  # Python < 3.12 has no `filter` kwarg
    except tarfile.TarError as e:
        print(f'  failed to extract {version}: {e}', file=sys.stderr)
        return None
    finally:
        tarball.unlink(missing_ok=True)  # reclaim disk before/while syft runs
    sbom = run_syft(extract_dir)
    if sbom is None:
        print(f'  syft scan failed for {version}', file=sys.stderr)
    return sbom


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('versions', nargs='*',
                         help='Specific Solr versions to refresh (default: all)')
    parser.add_argument('--verbose', action='store_true',
                         help='List every untracked dependency seen, not just the count')
    parser.add_argument('--slim', action='store_true',
                         help='Scan the smaller "-slim" distribution (9.x+ only, falls back to '
                              'full) instead of the full one. Faster, but misses dependencies '
                              'that only live in optional modules (Hadoop, Tika/extraction, etc).')
    args = parser.parse_args()

    all_versions = [
        ln.strip() for ln in VERSIONS_FILE.read_text().splitlines()
        if ln.strip() and not ln.strip().startswith('#')
    ]
    versions = args.versions or all_versions
    unknown = sorted(set(versions) - set(all_versions))
    if unknown:
        sys.exit(f'Unknown Solr version(s), not in {VERSIONS_FILE.name}: {", ".join(unknown)}')

    dep_versions = json.loads(DEP_VERSIONS_FILE.read_text())
    tracked = set(dep_versions)
    new_candidates = {}
    conflicts = []
    skipped = []
    added = 0

    for i, version in enumerate(versions, 1):
        print(f'[{i}/{len(versions)}] Solr {version}...', file=sys.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            sbom = scan_version(version, Path(tmp), slim=args.slim)
        if sbom is None:
            skipped.append(version)
            continue

        found_this_version = {}
        for group, artifact, dep_version in iter_maven_packages(sbom):
            key = f'{group}:{artifact}'
            if key in tracked:
                found_this_version.setdefault(key, dep_version)
            elif group not in EXCLUDED_GROUPS:
                new_candidates.setdefault(key, set()).add(version)

        # Only fill genuine gaps -- never overwrite an existing value. A
        # resolved value that disagrees with what's already on file is
        # surfaced as a conflict for a human to look into, never applied
        # automatically.
        for key, dep_version in found_this_version.items():
            existing = dep_versions.setdefault(key, {})
            if version not in existing:
                existing[version] = dep_version
                added += 1
            elif existing[version] != dep_version:
                conflicts.append((key, version, existing[version], dep_version))

        DEP_VERSIONS_FILE.write_text(json.dumps(dep_versions, indent=2) + '\n')

    print(f'\nUpdated {DEP_VERSIONS_FILE.relative_to(REPO_ROOT)}: filled {added} missing '
          f'(dependency, version) entries.', file=sys.stderr)

    if skipped:
        print(f'\n{len(skipped)} version(s) skipped (no release tarball found, or '
              f'extraction/scan failed): {", ".join(skipped)}', file=sys.stderr)

    if conflicts:
        print(f'\n{len(conflicts)} resolved value(s) disagree with what is already on file '
              f'-- left UNCHANGED, please review by hand:', file=sys.stderr)
        for key, version, existing_value, resolved_value in conflicts:
            print(f'  {key} @ {version}: on file = {existing_value!r}, '
                  f'resolved = {resolved_value!r}', file=sys.stderr)

    if new_candidates:
        print(f'\n{len(new_candidates)} dependencies seen but not yet tracked '
              f'(rerun with --verbose to list them; add to solr-dependency-versions.json '
              f'if one becomes security-relevant).', file=sys.stderr)
        if args.verbose:
            for key in sorted(new_candidates):
                print(f'  {key}', file=sys.stderr)


if __name__ == '__main__':
    main()
