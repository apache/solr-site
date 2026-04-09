Title: Solr™ CVE Status for Dependencies
URL: security-dependency-cves.html
save_as: security-dependency-cves.html
template: security-dependency-cves

Apache Solr depends on many third-party libraries. Security scanners routinely flag CVEs in
those libraries, but a CVE in a dependency does not automatically mean Solr is vulnerable —
it depends on whether Solr actually exercises the affected code path in a way that can be exploited.

We publish our assessment of dependency CVEs in a machine-readable
**[VEX (Vulnerability Exploitability eXchange)](https://cyclonedx.org/capabilities/vex/)** file.
VEX is an open standard that lets vendors state explicitly whether a CVE applies to their product,
and why. A number of formats are under active development, including
[CycloneDX](https://cyclonedx.org/capabilities/vex/) and
[CSAF](https://github.com/oasis-tcs/csaf/blob/master/csaf_2.0/prose/csaf-v2-editor-draft.md#45-profile-5-vex).
We currently publish in CycloneDX 1.4 JSON format.

If your scanner supports VEX, download the file below and point your scanner at it to automatically
suppress known non-applicable findings. If your scanner does not yet support VEX, you can use the
table on this page to manually triage flagged CVEs.

We encourage feedback on VEX and tool support — join the discussion at
[security-discuss@community.apache.org](mailto:security-discuss@community.apache.org)
or contact [security@apache.org](mailto:security@apache.org).
