import os
import json
from re import sub
from uuid import UUID, uuid5
from hashlib import md5
from pathlib import Path
from pelican import signals
from jsonschema import validate
import jsonref

def __get_vex_input():
    input_dir = Path("vex-input")
    vex_input = []
    if not input_dir.exists():
        raise FileNotFoundError("`vex-input` folder not found")
    for path in sorted(input_dir.glob('*.json')):
        with path.open('r', encoding='utf-8') as f:
            data = json.load(f)
            vex_input.append(data)
    return vex_input

def pelican_init(pelicanobj):
    vex_input = __get_vex_input()

    # Our own input format - feel free to change as needed,
    # but remember to also update this plugin and the templates in
    # /themes/solr/templates/security.html
    with open('plugins/vex/schema/vex-input.schema.json', 'r') as file:
        loaded = jsonref.load(file, base_uri=Path('./plugins/vex/schema/base').absolute().as_uri())
        validate(vex_input, loaded)

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
        "specVersion": "1.4",
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
    with open('plugins/vex/schema/bom-1.4.schema.json', 'r') as schema:
        validate(vex, json.load(schema))

    output_path = pelicanobj.settings['OUTPUT_PATH']
    os.makedirs(output_path, exist_ok=True)
    with open('%s/solr.vex.json' % output_path, 'w') as out:
        json.dump(vex, out, indent=2)


def generator_initialized(generator):
    generator.context["vex"] = __get_vex_input()
    generator.context["sub"] = sub


def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
    signals.generator_init.connect(generator_initialized)
