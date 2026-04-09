Title: Solr™ Security
URL: security.html
save_as: security.html
template: security

## Report a New Vulnerability

The Solr PMC greatly appreciates responsible disclosure of new security vulnerabilities found in Solr itself
or demonstrating exploitation via a dependency.

See the [vulnerability reporting procedure](security-reporting.html) for the full reporting rules,
the workflow diagram, and what to expect after you report.

## CVEs in Dependencies Detected by Scanners

Every CVE detected by a scanner is by definition already public knowledge.
Before contacting the security team about a dependency CVE, please:

1. Check the [dependency CVE status page](security-dependency-cves.html) to see if the CVE has already
   been assessed as not exploitable in Solr.
2. Download our [VEX file](security-dependency-cves.html) if your scanner supports VEX, to automatically suppress known non-applicable findings.
3. Search the [Solr users mailing list archive](https://lists.apache.org/list.html?users@solr.apache.org)
   to see if the CVE has been discussed.
4. If nothing is found, [subscribe to the users list](https://solr.apache.org/community.html#mailing-lists-chat)
   and ask there.

#### Dos and Don'ts

* **DO** discuss dependency upgrade needs on the users mailing list
* **DO** search Jira for the CVE number before opening a new issue
* **DO** open a focused Jira issue with a PR to upgrade a *single specific* dependency
* **DO NOT** email the security address with scanner reports — they will not be processed
* **DO NOT** paste scan output into Jira or attach reports — link the CVE instead

