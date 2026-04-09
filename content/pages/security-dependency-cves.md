Title: Solr™ CVE Status for Dependencies
URL: security-dependency-cves.html
save_as: security-dependency-cves.html
template: security-dependency-cves

Apache Solr depends on many third-party libraries. Security scanners routinely flag CVEs in
those libraries, but a CVE in a dependency does not automatically mean Solr is vulnerable —
it depends on whether Solr actually exercises the affected code path in a way that can be exploited.

We publish our assessment of dependency CVEs in a machine-readable
**[VEX (Vulnerability Exploitability eXchange)](https://cyclonedx.org/capabilities/vex/)** file.
VEX is an emerging standard that lets vendors state explicitly whether a CVE applies to their product,
and why. Our file follows the [CycloneDX 1.4](https://cyclonedx.org/) JSON format.

If your scanner supports VEX, download the file below and point your scanner at it to automatically
suppress known non-applicable findings. If your scanner does not yet support VEX, you can use the
table on this page to manually triage flagged CVEs.

We encourage feedback on VEX and tool support — join the discussion at
[security-discuss@community.apache.org](mailto:security-discuss@community.apache.org)
or contact [security@apache.org](mailto:security@apache.org).
