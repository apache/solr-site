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

<h2 id="before-you-report">Before You Report <a class="headerlink" href="#before-you-report" title="Permanent link">¶</a></h2>

Ensure you have tested against a [supported Solr version](https://solr.apache.org/downloads.html)
with both **authentication** and **authorization** properly configured.
Solr's admin level APIs are designed to be used only by authenticated and trusted administrators.

<h2 id="submission-rules">Submission Rules <a class="headerlink" href="#submission-rules" title="Permanent link">¶</a></h2>

A valid security report to [security@solr.apache.org](mailto:security@solr.apache.org) must:

1. **Be sent as plaintext** — no zip file attachments, no links to Google Docs, Dropbox, or similar services
2. **Cover exactly one vulnerability** — if you have multiple findings, send one email per issue
3. **Include step-by-step reproduction steps** — scanner output or LLM generated reports are not sufficient by themselves.
4. **Demonstrate the issue with authentication and authorization enabled** — running Solr
   without authentication is a misconfiguration, not a vulnerability
5. **Target a [supported Solr version](https://solr.apache.org/downloads.html)** — reports
   against unsupported versions will not be accepted

<h2 id="workflow">Workflow <a class="headerlink" href="#workflow" title="Permanent link">¶</a></h2>

<pre class="mermaid">
flowchart TD
    A["`**Submit security report**
  *Plaintext · one issue*
  *repro steps · auth enabled*
  security@solr.apache.org`"]

    D["`**PMC triage**
  *up to 7 days*`"]

    E["`**Rejected**
  *No repro / no auth*
  *zip or link / multiple issues*`"]

    F["`**Needs changes**
  *PMC requests clarification*`"]

    G["`**Accepted**
  *ACK email + private JIRA*
  *within 7 days*`"]

    I["`**Full investigation**
  *up to 90 days*`"]

    J["`**Won't fix**
  *Reporter notified*`"]

    K["`**Fix & coordinated disclosure**
  *CVE published*
  *reporter credited in advisory*`"]

    A --> D
    D -->|rejected| E
    D -->|needs changes| F
    D -->|accepted| G
    F -->|revise & re-send| A
    G --> I
    I -->|not confirmed| J
    I -->|confirmed| K

    classDef submit    fill:#eae6f5,stroke:#9b93d0,color:#3d3a6b
    classDef process   fill:#fdf4e8,stroke:#c8a86b,color:#5a4520
    classDef rejected  fill:#fde8e8,stroke:#d08080,color:#7a2020
    classDef changes   fill:#fdefd8,stroke:#d4a060,color:#7a4010
    classDef accepted  fill:#dff5ec,stroke:#6dbfa0,color:#1a5a40
    classDef wontfix   fill:#fde8e8,stroke:#d08080,color:#7a2020
    classDef disclosure fill:#f5f0e0,stroke:#b8ad80,color:#4a4020

    class A submit
    class D,G,I process
    class E rejected
    class F changes
    class J wontfix
    class K disclosure
</pre> 

<h2 id="what-to-expect">What to Expect <a class="headerlink" href="#what-to-expect" title="Permanent link">¶</a></h2>

| Step | Who | Timeframe |
|------|-----|-----------|
| Initial triage / acknowledgment | PMC volunteers | Up to 7 days |
| Full investigation | PMC volunteers | Up to 90 days |
| CVE ID allocation | PMC + ASF Security Team (CNA) | During fix development |
| Fix + CVE publication | PMC + ASF Security Team | Coordinated with you, the reporter |
| Credit in advisory | PMC | At public disclosure |

Public disclosure follows the [ASF standard process](https://www.apache.org/security/committers.html) and is announced on the
[oss-security mailing list](https://oss-security.openwall.org/wiki/mailing-lists/oss-security).

---
**For PMC members:** The following section documents the internal triage process and provides email templates for responding to incoming reports.

<h2 id="canned-responses">Canned Email Responses <a class="headerlink" href="#canned-responses" title="Permanent link">¶</a></h2>

The following templates are provided for PMC members responding to incoming reports.
Click each entry to expand and view the template.

<details>
<summary>Response A: Acknowledgment — report received and under review</summary>
<pre>
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

Please read https://solr.apache.org/security-reporting.html for the full process.

Apache Solr Security Team
</pre>
</details>

<details>
<summary>Response C: Reject — multiple distinct vulnerabilities in one email</summary>
<pre>
Thank you for your security report.

Your email appears to describe several separate potential vulnerabilities.
To allow each issue to be tracked, fixed, and disclosed independently,
please re-submit each as a separate email to security@solr.apache.org.

Each email should cover exactly one vulnerability with:
  - A clear description of the issue
  - Step-by-step reproduction instructions
  - The Solr version tested
  - The impact and attack scenario

We will begin reviewing each issue once we receive the separate reports.

Please read https://solr.apache.org/security-reporting.html for the full process.

Apache Solr Security Team
</pre>
</details>

<details>
<summary>Response D: Reject — report sent as zip file or external link</summary>
<pre>
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

Please read https://solr.apache.org/security-reporting.html for the full process.

Apache Solr Security Team
</pre>
</details>

<details>
<summary>Response E: Reject — no authentication configured or behavior within expected role</summary>
<pre>
Thank you for your security report.

After reviewing your report, we are unable to treat this as a security
vulnerability due to either of the following reasons:

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

Please read https://solr.apache.org/security-reporting.html for the full process.

Apache Solr Security Team
</pre>
</details>

<h2 id="pmc-process">After Acceptance: PMC Process <a class="headerlink" href="#pmc-process" title="Permanent link">¶</a></h2>

Once a report passes initial triage, the PMC follows these steps:

1. Create a **private JIRA issue** with the appropriate security level (not publicly visible)
2. Send the **acknowledgment email** to the reporter (Response A above)
3. PMC coordinates the investigation through private channels
4. When a fix is ready, request a **CVE ID from the ASF Security Team**, via the CVE portal
5. **Notify the reporter** of the chosen fix and planned disclosure date
6. **Publish the fix release**, then publish the CVE advisory on the security page
7. The ASF Security Team announces the advisory on **oss-security@lists.openwall.com**
8. **Update security-news** page with the new CVE entry and close the JIRA issue
