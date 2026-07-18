import glob
import json
import os
import re
from hashlib import md5
from pathlib import Path
from uuid import UUID, uuid5

import jsonref
from jsonschema import ValidationError, validate
from pelican import signals
from strictyaml import load
from strictyaml.ruamel import YAML

SCHEMA_DIR = Path(__file__).resolve().parent / 'schema'

# Lazily loaded, ref-resolved JSON Schema for VEX Markdown front matter.
_article_schema = None


def article_schema():
    """Load plugins/vex/schema/vex_article.schema.yaml, resolving its $ref into
    bom-1.6.schema.json. Cached after the first call."""
    global _article_schema
    if _article_schema is None:
        raw = (SCHEMA_DIR / 'vex_article.schema.yaml').read_text()
        schema = YAML(typ='safe').load(raw)
        _article_schema = jsonref.replace_refs(
            schema, base_uri=SCHEMA_DIR.as_uri() + '/')
    return _article_schema


def vex_anchor(path):
    """Unique per-entry anchor/slug derived from the source filename: the stem
    without the leading 'YYYY-MM-DD-' date prefix and the '.md' extension.

    Used both for the on-page anchors and as each VEX article's slug, because
    titles repeat across entries (e.g. 'log4j-core') while filenames are unique.
    """
    return os.path.basename(path)[11:-3]


def split_front_matter(path):
    """Return (front_matter, body) for a Markdown file with YAML front matter.

    The front matter is the text between the leading '---' line and the next
    '---' line. Returns (None, full_text) when the file has no front matter.
    """
    with open(path, 'r') as f:
        text = f.read()
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return None, text
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            return '\n'.join(lines[1:i]), '\n'.join(lines[i + 1:])
    raise ValueError(f"Unterminated YAML front matter in {path}")


def read_vex_articles(content_path):
    """Parse the VEX Markdown files under <content_path>/solr/vex/.

    Each file's YAML front matter supplies the CVE id(s) (the 'cve' field may be a
    single id or a list) and the CycloneDX 'analysis' block; the Markdown body is
    used as the analysis 'detail' when the front matter omits it. Dependency CVEs
    additionally carry 'versions' (a display string of affected Solr versions) and
    'jars' (the vulnerable JAR files).

    Returns a list of entries shaped as
    {'ids': [...], 'analysis': {...}, 'versions': str, 'jars': [...]}.
    """
    articles = []
    vex_dir = os.path.join(content_path, 'solr', 'vex')
    for path in sorted(glob.glob(os.path.join(vex_dir, '*.md'))):
        front_matter, body = split_front_matter(path)
        if front_matter is None:
            continue
        meta = load(front_matter).data
        try:
            validate(instance=meta, schema=article_schema())
        except ValidationError as e:
            raise ValueError(
                'Invalid VEX front matter in %s: %s' % (path, e.message)) from e
        # 'cve' may be absent (catch-all dependency notes), a single id, or a list
        cve = meta.get('cve') or []
        ids = cve if isinstance(cve, list) else [cve]
        analysis = dict(meta['analysis'])
        if 'detail' not in analysis and body.strip():
            analysis['detail'] = body.strip()
        articles.append({
            'ids': ids,
            'analysis': analysis,
            'versions': meta.get('versions', ''),
            'jars': meta.get('jars', []),
            'title': meta.get('title', ''),
            # Anchor on vex.html (matches each VEX article's slug, see set_vex_slug).
            'anchor': vex_anchor(path),
            # "YYYY-MM-DD" filename date prefix, used for OpenVEX timestamps.
            'date': os.path.basename(path)[:10],
        })
    return articles


def pelican_init(pelicanobj):
    # The list of vulnerabilities is derived from the VEX Markdown files under
    # content/solr/vex/ (see read_vex_articles). The generated CycloneDX
    # document below is validated against bom-1.6.schema.json.
    vex_input = read_vex_articles(pelicanobj.settings['PATH'])

    ns = UUID('4f298c2c-eb7c-4968-a827-1482b1e5c095')
    ref = str(uuid5(ns, md5(json.dumps(vex_input).encode()).hexdigest()))

    vulns = []
    for v in vex_input:
        for id in v['ids']:
            source = {}
            if id.startswith("CVE"):
                # dependency-track uses 'NVD' as source name for CVEs
                # https://github.com/DependencyTrack/dependency-track/blob/8673aab774214300b45e9c8ee4f67a2dbed7514f/src/main/java/org/dependencytrack/model/Vulnerability.java#L102
                source['name'] = "NVD";
                source['url'] = f"https://nvd.nist.gov/vuln/detail/{id}"
            elif id.startswith("GHSA"):
                source['name'] = "GITHUB";
                source['url'] = f"https://github.com/advisories/{id}"

            vulns.append({
                "id": id,
                "source": source,
                "analysis": v['analysis'],
                "affects": [
                    {
                        "ref": ref
                    }
                ]
            })
    vex = {
        # we're not committing to doing exactly what CycloneDX comes
        # up with, but it seems like one of the promising formats, so
        # let's align with it as much as possible:
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {
            "component": {
                "name": "solr",
                "version": "SNAPSHOT",
                "type": "application",
                "bom-ref": ref
            }
        },
        "vulnerabilities": vulns
    }
    # From https://github.com/CycloneDX/specification/tree/master/schema
    with open('plugins/vex/schema/bom-1.6.schema.json', 'r') as schema:
        validate(vex, json.load(schema))

    output_path = pelicanobj.settings['OUTPUT_PATH']
    os.makedirs(output_path, exist_ok=True)
    with open('%s/solr.vex.json' % output_path, 'w') as out:
        json.dump(vex, out, indent=2)

    # OpenVEX (https://openvex.dev/) output, derived from the same entries and
    # validated against the vendored OpenVEX JSON schema.
    openvex = build_openvex(vex_input)
    with open(SCHEMA_DIR / 'openvex_json_schema.json') as schema:
        validate(openvex, json.load(schema))
    with open('%s/solr.openvex.json' % output_path, 'w') as out:
        json.dump(openvex, out, indent=2)


# --- OpenVEX generation -----------------------------------------------------

# CycloneDX analysis.state -> OpenVEX status vocabulary.
OPENVEX_STATUS = {
    'not_affected': 'not_affected',
    'exploitable': 'affected',
    'in_triage': 'under_investigation',
    'resolved': 'fixed',
}

# CycloneDX analysis.justification -> OpenVEX justification, for the cases that
# have a clean equivalent. 'requires_configuration' has no OpenVEX counterpart,
# so those not_affected statements rely on impact_statement instead.
OPENVEX_JUSTIFICATION = {
    'code_not_present': 'vulnerable_code_not_present',
    'code_not_reachable': 'vulnerable_code_not_in_execute_path',
}

# Maven groupIds for the artifacts our VEX entries reference, so a JAR name can
# be emitted as a proper purl subcomponent. Artifacts not listed here (or JARs
# whose version can't be parsed, e.g. "guava-*.jar") fall back to a bare @id.
JAR_GROUPS = {
    'opennlp-tools': 'org.apache.opennlp',
    'jetty-http': 'org.eclipse.jetty',
    'jetty-server': 'org.eclipse.jetty',
    'json-path': 'com.jayway.jsonpath',
    'zookeeper': 'org.apache.zookeeper',
    'xercesImpl': 'xerces',
    'protobuf-java': 'com.google.protobuf',
    'commons-beanutils': 'commons-beanutils',
    'commons-compress': 'org.apache.commons',
    'commons-configuration2': 'org.apache.commons',
    'commons-lang3': 'org.apache.commons',
    'commons-text': 'org.apache.commons',
    'dom4j': 'dom4j',
    'avatica-core': 'org.apache.calcite.avatica',
    'calcite': 'org.apache.calcite',
    'slf4j-api': 'org.slf4j',
    'icu4j': 'com.ibm.icu',
    'netty-all': 'io.netty',
    'netty-codec-compression': 'io.netty',
    'netty-codec-http': 'io.netty',
    'netty-codec-http2': 'io.netty',
    'netty-handler': 'io.netty',
    'netty-handler-proxy': 'io.netty',
    'netty-transport-native-epoll': 'io.netty',
    'netty-transport-native-unix-common': 'io.netty',
    'hadoop-auth': 'org.apache.hadoop',
    'hadoop-common': 'org.apache.hadoop',
    'log4j-core': 'org.apache.logging.log4j',
    'log4j-1.2-api': 'org.apache.logging.log4j',
    'log4j-layout-template-json': 'org.apache.logging.log4j',
    'lucene-analyzers-icu': 'org.apache.lucene',
    'vorbis-java-tika': 'org.gagravarr',
    'velocity-tools': 'org.apache.velocity',
    'org.restlet': 'org.restlet.jee',
    'simple-xml': 'org.simpleframework',
    'carrot2-guava': 'org.carrot2.shaded',
    'junit': 'junit',
    'guava': 'com.google.guava',
    'jackson-databind': 'com.fasterxml.jackson.core',
    'jdom': 'org.jdom',
    'jdom2': 'org.jdom',
    'tika-core': 'org.apache.tika',
    'calcite': 'org.apache.calcite',
    'calcite-core': 'org.apache.calcite',
    'jcl-over-slf4j': 'org.slf4j',
    'jul-to-slf4j': 'org.slf4j',
    'hadoop-hdfs': 'org.apache.hadoop',
    'hadoop-client': 'org.apache.hadoop',
    'simple-xml': 'org.simpleframework',
}

# Split a JAR name into (artifact, version). Standard `artifact-version.jar` uses
# a greedy artifact so the version is the *last* "-<digits...>" segment (handles
# artifacts that themselves contain version-like parts, e.g. `log4j-1.2-api`).
# The dot-separated form (`tika-core.1.17.jar`) is a rare fallback.
_JAR_HYPHEN_RE = re.compile(r'^(.+)-(\d[\w.]*)\.jar$')
_JAR_DOT_RE = re.compile(r'^(.+?)\.(\d[\w.]*)\.jar$')


def jar_to_component(jar):
    """Turn a vulnerable-JAR name into an OpenVEX subcomponent: a Maven purl when
    the coordinates are known, otherwise a bare @id using the raw name (e.g. for
    wildcard or descriptive entries like `guava-*.jar` or `jetty-9.4.6 to 9.4.36`)."""
    match = _JAR_HYPHEN_RE.match(jar) or _JAR_DOT_RE.match(jar)
    if match:
        artifact, version = match.group(1), match.group(2)
        group = JAR_GROUPS.get(artifact)
        if group:
            return {'@id': 'pkg:maven/%s/%s@%s' % (group, artifact, version)}
    return {'@id': jar}


def jar_coordinates(jar):
    """Parse a JAR name into (group, artifact) when the group is known, else None.
    The version in the JAR name is ignored — callers derive the concrete versions
    Solr actually shipped from solr-dependency-versions.json."""
    match = _JAR_HYPHEN_RE.match(jar) or _JAR_DOT_RE.match(jar)
    if not match:
        return None
    artifact = match.group(1)
    group = JAR_GROUPS.get(artifact)
    return (group, artifact) if group else None


DEP_VERSIONS_FILE = Path(__file__).resolve().parent / 'solr-dependency-versions.json'
_dep_versions = None


def dep_versions():
    """Load the {'group:artifact': {solr_version: dep_version}} map that records
    which version of each dependency every Solr release shipped."""
    global _dep_versions
    if _dep_versions is None:
        _dep_versions = json.loads(DEP_VERSIONS_FILE.read_text())
    return _dep_versions


# Authoritative list of every released Solr version, used to expand the
# free-form `versions` ranges into concrete per-version purls for OpenVEX.
VERSIONS_FILE = Path(__file__).resolve().parent / 'solr-versions.txt'
_solr_versions = None
_INF = 10 ** 9


def solr_versions():
    global _solr_versions
    if _solr_versions is None:
        _solr_versions = [
            ln.strip()
            for ln in VERSIONS_FILE.read_text().splitlines()
            if ln.strip() and not ln.strip().startswith('#')
        ]
    return _solr_versions


def _vkey(version):
    """Concrete version string -> comparable 4-tuple (missing parts default to 0)."""
    parts = [int(re.match(r'\d+', p).group()) for p in version.split('.') if re.match(r'\d+', p)]
    return tuple((parts + [0, 0, 0, 0])[:4])


def _token_bounds(token):
    """A version token -> (low, high) inclusive keys it covers. Fewer components
    or a trailing '.x' widen it to the whole line: '9.9.0' is exact, '9.10' is the
    9.10.x line, '8.x' is the whole 8.x major line."""
    token = token.strip()
    wildcard = token.endswith('.x')
    core = token[:-2] if wildcard else token
    parts = [int(re.match(r'\d+', p).group()) for p in core.split('.') if re.match(r'\d+', p)]
    low = tuple((parts + [0, 0, 0, 0])[:4])
    if not wildcard and len(parts) >= 3:      # fully-specified version -> exact
        return low, low
    return low, tuple((parts + [_INF, _INF, _INF, _INF])[:4])


def _matches_token(vk, tok):
    tok = tok.strip()
    if tok.startswith('≤') or tok.startswith('<='):
        return vk <= _token_bounds(tok.lstrip('≤<= ').strip())[1]
    if tok.startswith('<'):
        return vk < _token_bounds(tok.lstrip('< ').strip())[0]
    if tok.startswith('≥') or tok.startswith('>='):
        return vk >= _token_bounds(tok.lstrip('≥>= ').strip())[0]
    if '-' in tok:
        a, b = tok.split('-', 1)
        return _token_bounds(a)[0] <= vk <= _token_bounds(b)[1]
    low, high = _token_bounds(tok)
    return low <= vk <= high


def expand_versions(range_str):
    """Expand a `versions` range string (e.g. '4.6.0-8.x') into the concrete
    released Solr versions it covers.

    Only fully-closed ranges are expanded. Ranges with an open lower bound
    ('≤'/'<'), and 'all'/empty ranges, return [] so the caller falls back to a
    version-less product purl. Without a real lower bound, expansion would run
    back to the earliest release (1.1.0) and over-claim versions that predate the
    affected dependency. (Closing those bounds is a follow-up in the VEX data.)"""
    if not range_str or range_str.strip() == 'all':
        return []
    tokens = range_str.split(',')
    if any(t.strip().startswith(('≤', '<')) for t in tokens):
        return []
    return [v for v in solr_versions() if any(_matches_token(_vkey(v), t) for t in tokens)]


def jar_products(jars, versions):
    """Turn an entry's vulnerable JARs into OpenVEX product purls.

    A single VEX statement must match a dependency across every Solr image in the
    affected range, but each Solr release ships a different pinned version of that
    dependency. So for each JAR whose coordinates are known, we expand it to a purl
    per concrete dependency version Solr actually shipped over the affected Solr
    range (from solr-dependency-versions.json), rather than the single version in
    the JAR name. JARs we can't resolve (unknown group, open-lower-bound range, or a
    dependency not in the map) fall back to the literal purl from the JAR name."""
    affected_solr = expand_versions(versions)
    products, seen = [], set()

    def add(component):
        if component['@id'] not in seen:
            seen.add(component['@id'])
            products.append(component)

    for jar in jars:
        coords = jar_coordinates(jar)
        shipped = dep_versions().get('%s:%s' % coords) if coords else None
        derived = sorted({shipped[sv] for sv in affected_solr if sv in shipped}) \
            if (coords and shipped and affected_solr) else []
        if derived:
            group, artifact = coords
            for ver in derived:
                add({'@id': 'pkg:maven/%s/%s@%s' % (group, artifact, ver)})
        else:
            add(jar_to_component(jar))
    return products


def build_openvex(entries):
    """Build an OpenVEX (v0.2.0) document from read_vex_articles() entries.

    The vulnerable JAR purls are emitted as the statement `products`, because
    scanners (e.g. Docker Scout) match VEX on the product purl of the affected
    package. Entries with no JAR (Solr-native CVEs) use the Solr product instead,
    version-expanded from a closed range (via solr-versions.txt) or version-less
    for an open lower bound. The Solr version range is preserved in status_notes.
    """
    statements = []
    for v in entries:
        if not v['ids']:
            continue
        status = OPENVEX_STATUS.get(v['analysis']['state'], 'under_investigation')
        detail = (v['analysis'].get('detail') or '').strip()

        vulnerability = {'name': v['ids'][0]}
        if len(v['ids']) > 1:
            vulnerability['aliases'] = v['ids'][1:]

        # Scanners (e.g. Docker Scout) match VEX statements on the product purl,
        # so the vulnerable JAR(s) are the products. For an entry with no JAR
        # (e.g. a Solr-native CVE), the product is Solr itself: a versioned purl
        # per affected release when the range is closed, else version-less. The
        # human-readable Solr version range is carried in status_notes below.
        if v['jars']:
            products = jar_products(v['jars'], v['versions'])
        else:
            affected = expand_versions(v['versions'])
            if affected:
                products = [{'@id': 'pkg:maven/org.apache.solr/solr-core@%s' % ver} for ver in affected]
            else:
                products = [{'@id': 'pkg:maven/org.apache.solr/solr-core'}]

        statement = {
            'vulnerability': vulnerability,
            'products': products,
            'status': status,
            'timestamp': '%sT00:00:00Z' % v['date'],
        }
        notes = ('Affected Apache Solr versions: %s.' % v['versions']) if v['versions'] else ''

        if status == 'not_affected':
            justification = OPENVEX_JUSTIFICATION.get(v['analysis'].get('justification'))
            if justification:
                statement['justification'] = justification
            # OpenVEX requires a justification or impact_statement for not_affected.
            statement['impact_statement'] = detail or 'Apache Solr is not affected.'
            if notes:
                statement['status_notes'] = notes
        elif status == 'affected':
            statement['action_statement'] = detail or 'Update to a fixed release of Apache Solr.'
            if notes:
                statement['status_notes'] = notes
        else:  # under_investigation / fixed
            combined = ' '.join(part for part in (notes, detail) if part)
            if combined:
                statement['status_notes'] = combined

        statements.append(statement)

    newest = max((v['date'] for v in entries), default='1970-01-01')
    return {
        '@context': 'https://openvex.dev/ns/v0.2.0',
        '@id': 'https://solr.apache.org/solr.openvex.json',
        'author': 'Apache Solr Project (security@apache.org)',
        'timestamp': '%sT00:00:00Z' % newest,
        'version': 1,
        'statements': statements,
    }

def generator_initialized(generator):
    # The dependency-CVE table (security-dependency-cves.html) lists the entries
    # that declare vulnerable JARs, in all states (including exploitable).
    # Advisory-only entries without 'jars' (e.g. Solr-native CVEs) are excluded.
    articles = read_vex_articles(generator.settings['PATH'])
    generator.context["vex"] = [a for a in articles if a['jars']]


def set_vex_slug(content):
    """Give each VEX article a unique slug from its filename, so entries that
    share a title (e.g. two 'log4j-core' CVEs) don't collide on slug."""
    category = getattr(content, 'category', None)
    if category is not None and category.name == 'solr/vex':
        content.slug = vex_anchor(content.source_path)


def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
    signals.generator_init.connect(generator_initialized)
    signals.content_object_init.connect(set_vex_slug)
