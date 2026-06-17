import glob
import json
import os
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


def generator_initialized(generator):
    # The CVE table (security-dependency-cves.html) lists every VEX entry.
    generator.context["vex"] = read_vex_articles(generator.settings['PATH'])


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
