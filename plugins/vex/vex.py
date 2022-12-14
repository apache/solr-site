import os
import sys
import json
from re import sub
from uuid import UUID, uuid5
from hashlib import md5
from pelican import signals
from jsonschema import validate
import jsonref

def pelican_init(pelicanobj):
    with open('vex-input.json', 'r') as input:
        vex_input = json.loads(input.read())

    # Our own input format - feel free to change as needed,
    # but remember to also update this plugin and the templates in
    # /themes/solr/templates/security.html
    with open('plugins/vex/schema/vex-input.schema.json', 'r') as file:
        from pathlib import Path
        loaded = jsonref.load(file, base_uri=Path('./plugins/vex/schema/base').absolute().as_uri())
        validate(vex_input, loaded)

    ns = UUID('4f298c2c-eb7c-4968-a827-1482b1e5c095')
    ref = str(uuid5(ns, md5(json.dumps(vex_input).encode()).hexdigest()))

    vulns = []
    for v in vex_input:
        for id in v['ids']:
            vulns.append({
                "id": id,
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

    os.makedirs('output', exist_ok=True)
    with open('output/solr.vex.json', 'w') as out:
        json.dump(vex, out, indent=2)

def generator_initialized(generator):
    generator.context["vex"] = json.load(open('vex-input.json'))
    generator.context["sub"] = sub

def register():
    """Plugin registration"""
    signals.initialized.connect(pelican_init)
    signals.generator_init.connect(generator_initialized)
