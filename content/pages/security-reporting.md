Title: Solr™ Vulnerability Reporting Procedure
URL: security-reporting.html
save_as: security-reporting.html
template: security-reporting

This page documents the procedure for reporting a security vulnerability in Apache Solr and
explains what happens after a report is submitted. It also provides canned email templates
for PMC members to use when responding to reports.

Apache Solr is maintained by volunteers. The PMC will make every effort to respond promptly,
but cannot guarantee specific response times. We appreciate your patience and your contribution
to the security of the project.

If you have concerns about how the project team is handling a report, you may also contact
[security@apache.org](mailto:security@apache.org) directly.
For PMC members, the ASF provides detailed
[committer guidance on vulnerability handling](https://www.apache.org/security/committers.html).

## Before You Report

Ensure you have tested against a [supported Solr version](https://solr.apache.org/downloads.html)
with both **authentication** and **authorization** properly configured.
Exploits demonstrated without authentication are not valid — running Solr without authentication is a
misconfiguration, not a vulnerability.

<h2 id="submission-rules">Submission Rules <a class="headerlink" href="#submission-rules" title="Permanent link">¶</a></h2>

A valid security report to [security@solr.apache.org](mailto:security@solr.apache.org) must:

1. **Be sent as plaintext** — no zip file attachments, no links to Google Docs, Dropbox, or similar services
2. **Cover exactly one vulnerability** — if you have multiple findings, send one email per issue
3. **Include step-by-step reproduction steps** — scanner output alone is not a report
4. **Demonstrate the issue with authentication and authorization enabled** — running Solr
   without authentication is a misconfiguration, not a vulnerability
5. **Target a [supported Solr version](https://solr.apache.org/downloads.html)** — reports
   against unsupported versions will not be accepted

<h2 id="workflow">Workflow <a class="headerlink" href="#workflow" title="Permanent link">¶</a></h2>

<figure class="workflow-figure">
  <img src="{{ SITEURL }}/theme/images/security-vuln-process.png"
       alt="Flowchart showing the Solr vulnerability reporting process: reporter submits plaintext email, PMC triages within 7 days (reject / needs changes / accepted), accepted reports get a private JIRA and ACK email, followed by full investigation up to 30 days, then either won't fix or confirmed vuln leading to fix, coordinated disclosure, CVE publication, and credit in advisory." />
  <figcaption>Solr vulnerability reporting workflow</figcaption>
</figure>

<h2 id="what-to-expect">What to Expect <a class="headerlink" href="#what-to-expect" title="Permanent link">¶</a></h2>

| Step | Who | Timeframe |
|------|-----|-----------|
| Initial triage / acknowledgment | PMC volunteers | Up to 7 days |
| Full investigation | PMC volunteers | Up to 30 days |
| CVE ID allocation | PMC + ASF Security Team (CNA) | During fix development |
| Fix + CVE publication | PMC + ASF Security Team | Coordinated with you, the reporter |
| Credit in advisory | PMC | At public disclosure |

Public disclosure follows the ASF standard process and is announced on the
[oss-security mailing list](https://oss-security.openwall.org/wiki/mailing-lists/oss-security).

<h2 id="canned-responses">Canned Email Responses <a class="headerlink" href="#canned-responses" title="Permanent link">¶</a></h2>

The following templates are provided for PMC members responding to incoming reports.
Click each entry to expand and copy the template.

<details>
<summary>Response A: Acknowledgment — report received and under review</summary>
<pre>
Subject: Re: [Original Subject]

Thank you for your security report.

We have received your report and created a private issue to track it.
The Solr PMC will review your report and aim to update you within 30 days.
We will keep you informed through this email thread.

Please do not discuss this report on public channels (mailing lists,
GitHub, social media) until we have coordinated public disclosure with you.

If you have additional information, please reply to this email.

Apache Solr Security Team
security@solr.apache.org
https://solr.apache.org/security.html
</pre>
</details>

<details>
<summary>Response B: Reject — scanner output without reproduction steps</summary>
<pre>
Subject: Re: [Original Subject]

Thank you for contacting the Solr security team.

We are unable to process reports that consist solely of scanner tool output
without a demonstrated reproduction of the vulnerability in Apache Solr.

Scanner reports list dependency CVEs that are often not applicable to how
Solr uses those libraries. Before filing a security report, please:

1. Check https://solr.apache.org/security-dependency-cves.html — we publish
   a VEX file listing CVEs already assessed as not exploitable in Solr.
2. Verify the issue is actually exploitable in a properly configured Solr
   instance (with authentication and authorization enabled).
3. Write step-by-step reproduction steps that demonstrate the impact on
   Solr specifically.

For dependency upgrade discussions, the public Solr users list is the
right venue: users@solr.apache.org

Apache Solr Security Team
</pre>
</details>

<details>
<summary>Response C: Reject — multiple distinct vulnerabilities in one email</summary>
<pre>
Subject: Re: [Original Subject]

Thank you for your security report.

Your email appears to describe [N] separate potential vulnerabilities.
To allow each issue to be tracked, fixed, and disclosed independently,
please re-submit each as a separate email to security@solr.apache.org.

Each email should cover exactly one vulnerability with:
  - A clear description of the issue
  - Step-by-step reproduction instructions
  - The Solr version tested
  - The impact and attack scenario

We will begin reviewing each issue once we receive the separate reports.

Apache Solr Security Team
</pre>
</details>

<details>
<summary>Response D: Reject — report sent as zip file or external link</summary>
<pre>
Subject: Re: [Original Subject]

Thank you for your security report.

For security reasons, the Solr PMC does not open zip file attachments
or follow external links (Google Docs, Dropbox, etc.) in security reports.

Please re-send your report as plaintext in the body of an email to
security@solr.apache.org, including:

  - Description of the vulnerability
  - Step-by-step reproduction instructions
  - Solr version and configuration tested
  - Expected vs. actual behavior
  - Any relevant log output, pasted directly into the email

We look forward to reviewing your report once re-submitted in plaintext.

Apache Solr Security Team
</pre>
</details>

<details>
<summary>Response E: Reject — no authentication configured or behavior within expected role</summary>
<pre>
Subject: Re: [Original Subject]

Thank you for your security report.

After reviewing your report, we are unable to treat this as a security
vulnerability because [choose applicable]:

  a) The behavior requires Solr to be running without authentication.
     Solr is not designed for unauthenticated operation in any networked
     environment. Running without authentication is a misconfiguration,
     not a Solr vulnerability.

  b) The action performed was permitted by the role used in your test.
     A vulnerability requires either that the action exceeded what the
     role should allow, or that it should never be permitted for any role.

If you believe our assessment is incorrect, please reply with details
explaining why the behavior should not be possible under your tested
configuration and role.

Apache Solr Security Team
</pre>
</details>

<h2 id="jira-process">After Acceptance: JIRA Process <a class="headerlink" href="#jira-process" title="Permanent link">¶</a></h2>

Once a report passes initial triage, the PMC follows these steps:

1. Create a **private JIRA issue** with the appropriate security level (not publicly visible)
2. Send the **acknowledgment email** to the reporter (Response A above)
3. The issue is included in the **weekly security-issues digest** email for PMC awareness
4. PMC coordinates the investigation via private JIRA, the security mailing list, and security Slack
5. When a fix is ready, request a **CVE ID from the ASF Security Team** (the CNA for all Apache projects) via the CVE portal
6. **Notify the reporter** of the planned disclosure date
7. **Publish the fix release**, then publish the CVE advisory on the security page
8. The ASF Security Team announces the advisory on **oss-security@lists.openwall.com**
9. **Update security.html** with the new CVE entry and close the JIRA issue
