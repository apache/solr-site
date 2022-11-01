Title: Solr™ Security News
URL: security.html
save_as: security.html
template: security

## How to report a security issue
Solr depends on lots of other open-source software -- "dependencies".  If a CVE is published (a publicly identified vulnerability) against one of them, the Solr project will review it to see if it's actually exploitable in Solr -- usually they aren't.  The non-exploitable vulnerabilities are published [on this Confluence page](https://cwiki.apache.org/confluence/display/SOLR/SolrSecurity#SolrSecurity-SolrandVulnerabilityScanningTools).  If you don't see a CVE there, ask us about it.
Then please disclose responsibly by following [these ASF guidelines](https://www.apache.org/security/) for reporting.

The Solr PMC will not accept the output of a vulnerability scan as a security report.
The main problem scanning tools have is that they doesn't know which vulnerabilities have been deemed non-exploitable based on how Solr (or other software) use them.
Consult the list above.
Please do not email the security list with issues on Solr dependencies or outputs from vulnerability scanning tools.

You may file your request by email to <mailto:security@solr.apache.org>.

## More information
You will find more security related information on our Wiki: <https://cwiki.apache.org/confluence/display/SOLR/SolrSecurity>, such as information on how to treat the automated reports from security scanning tools.

# Recent CVE reports for Apache Solr
Below is a list of already announced CVE vulnerabilities. These are also available as an [ATOM feed](/feeds/solr/security.atom.xml):
