Title: Solr™ Security News
URL: security.html
save_as: security.html
template: security

## How to report a security issue

### CVEs in Solr dependencies

The Solr PMC will not accept the output of a vulnerability scan as a security report.

Solr depends on lots of other open-source software -- "dependencies".
If a CVE is published (a publicly identified vulnerability) against one of them, the Solr project will review it to see if it's actually exploitable in Solr -- usually they aren't.
Please review the [officially published non-exploitable vulnerabilities](https://cwiki.apache.org/confluence/display/SOLR/SolrSecurity#SolrSecurity-SolrandVulnerabilityScanningTools) before taking any steps.
If you **don't** see a CVE there, you should take the following steps:

1. Search through the [Solr users mailing list](https://lists.apache.org/list.html?users@solr.apache.org) to see if anyone else has brought up this dependency CVE.
1. If no one has, then please do [subscribe to the users mailing list](https://solr.apache.org/community.html#mailing-lists-chat) and then send an email asking about the CVE.

### Exploits found in Solr

The Solr PMC greatly appreciates the reporting of security vulnerabilities found in Solr itself.

Then please disclose responsibly by following [these ASF guidelines](https://www.apache.org/security/) for reporting.
You may file your request by email to <mailto:security@solr.apache.org>.

## More information
You will find more security related information on our Wiki: <https://cwiki.apache.org/confluence/display/SOLR/SolrSecurity>, such as information on how to treat the automated reports from security scanning tools.

# Recent CVE reports for Apache Solr
Below is a list of already announced CVE vulnerabilities. These are also available as an [ATOM feed](/feeds/solr/security.atom.xml):
