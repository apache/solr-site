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
We publish this assessment in both **CycloneDX 1.6** and **OpenVEX** JSON formats (download links below).

If your scanner supports VEX, download the file below and point your scanner at it to automatically
suppress known non-applicable findings. If your scanner does not yet support VEX, you can use the
table on this page to manually triage flagged CVEs.

For example, [Docker Scout](https://docs.docker.com/scout/) can apply the OpenVEX file when scanning
an official Solr image:

```bash
# Download the OpenVEX file, then have Docker Scout apply it to a scan.
curl -sO https://solr.apache.org/solr.openvex.json
docker scout cves solr:9.9.0 --vex-location solr.openvex.json --vex-author '.*'
```

CVEs marked `not_affected` are then dropped from the results, while those marked `affected` remain.
(Solr's VEX is authored by the Apache Solr project, so `--vex-author '.*'` is required — by default
Docker Scout only trusts VEX statements authored by `*@docker.com`.)



We encourage feedback on VEX and tool support — join the discussion at
[security-discuss@community.apache.org](mailto:security-discuss@community.apache.org)
or contact [security@apache.org](mailto:security@apache.org).
