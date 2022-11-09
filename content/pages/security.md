Title: Solr™ Security News
URL: security.html
save_as: security.html
template: security

## How to report a security issue

### Published CVEs Detected by Scanners
Every CVE that is detected by a software scanner is by definition already public knowledge. That means the Solr PMC and the rest of the world probably already know about it.

To find a path forward in addressing a detected CVE we suggest the following process for fastest results:

1. Check further down this page to see if the CVE is listed as exploitable in Solr.
2. Check the [officially published non-exploitable vulnerabilities](https://cwiki.apache.org/confluence/display/SOLR/SolrSecurity#SolrSecurity-SolrandVulnerabilityScanningTools) list to see if the CVE is listed as not exploitable in Solr.
3. Search through the [Solr users mailing list archive](https://lists.apache.org/list.html?users@solr.apache.org)  to see if anyone else has brought up this dependency CVE.
4. If no one has, then please do [subscribe to the users mailing list](https://solr.apache.org/community.html#mailing-lists-chat) and then send an email asking about the CVE.

#### Dos and Don'ts
* Please DO discuss the possible need for library upgrades on the user list. 
* Please DO search Jira for the CVE number to see if we are addressing it already.
* Please DO create Jira issues and associated pull requests to propose and discuss upgrades of *a single specific* dependency.
* Please DO NOT attach a scan report, or paste output of a scan into Jira (just link the CVE instead)
* Please DO NOT email the security email below with a scan report it will be ignored.

#### Use of Jira
Jira is for discussing specific development modifications. Any Jira that contains only scan report output, or references multiple dependencies at the same time is likely to be ignored/closed. The large number of folks sending us reports of things that are already known is a serious drag on our (volunteer) time so **please search Jira** before opening a new issue. 

### New Exploits <span style="color:blue">You</span> Discover in Solr

The Solr PMC greatly appreciates reports of new security vulnerabilities found in Solr itself or demonstrations of exploiting vulnerabilities via dependencies.
**It is important not to publish a previously unknown exploit**, or exploit demonstration code on public mailing lists.
Please disclose new exploits responsibly by following these [ASF guidelines](https://www.apache.org/security/) for reporting.
The contact email for reporting newly discovered exploits in Solr is <mailto:security@solr.apache.org>.

Before reporting a new exploit ensure that you have tested it against an instance of Solr that has been properly configured with:

1. **Authentication** - Exploits demonstrated without login waste our time because Solr is not meant to run such that the entire world has access to all of its APIs. Running without forcing users to log in is no more valid than running linux with a widely known default root password, or a database with a root account that has no password.
2. **Authorization** - It is not an exploit unless the authenticated user was configured with a role that should have prohibited the action, or the action should never be allowed for any user regardless of role. Your report should say why you think this action is not acceptable for the role(s) you tested it with.

### More information
You will find more security related information on our Wiki: [https://cwiki.apache.org/confluence/display/SOLR/SolrSecurity](https://cwiki.apache.org/confluence/display/SOLR/SolrSecurity)

# Recent CVE reports for Apache Solr
Below is a list of already announced CVE vulnerabilities. These are also available as an [ATOM feed](/feeds/solr/security.atom.xml):
