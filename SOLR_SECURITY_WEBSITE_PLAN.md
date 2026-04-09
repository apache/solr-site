# Plan: SOLR-18193 Security Reporting Workflow Improvements

## Context
The Solr security page mixes CVE news, reporting guidance, VEX docs, and the full CVE table in one page.
SOLR-18193 asks to separate concerns, add visual workflow documentation, and create PMC canned responses.

Key constraints:
- Volunteer disclaimer appears only once
- Keep reporter-centric perspective; don't overload with ASF-internal process detail
- Link to https://www.apache.org/security/committers.html but keep it brief
- CVE IDs are assigned by ASF Security Team (CNA), not Solr PMC alone — reflect this accurately

---

## Branch
```
SOLR-18193-security-reporting-workflow
```

---

## Summary of Changes

| Action | File | Notes |
|--------|------|-------|
| MODIFY | `content/pages/security.md` | Rewrite/restructure; last 5 CVEs only; links to new sub-pages |
| MODIFY | `themes/solr/templates/security.html` | Trim CVE list to 5; add links to security-news |
| MODIFY | `plugins/combined_posts/__init__.py` | Add security-news paginated generation |
| CREATE | `themes/solr/templates/security-news.html` | Paginated security article history |
| MODIFY | `themes/solr/templates/posts.html` | Add Security News tab to subnav |
| CREATE | `content/pages/security-dependency-cves.md` | Dependency CVE status + VEX download |
| CREATE | `themes/solr/templates/security-dependency-cves.html` | VEX table + download button |
| CREATE | `content/pages/security-reporting.md` | PMC procedure + canned responses |
| CREATE | `themes/solr/templates/security-reporting.html` | Extends subnav.html |
| PLACE  | `themes/solr/static/images/security-vuln-process.png` | PNG diagram (placeholder; SVG to follow) |

---

## File Details

### 1. MODIFY: `plugins/combined_posts/__init__.py`

Add a second generator class `SecurityNewsGenerator` alongside `CombinedPostsGenerator`.
It filters only `solr/security` articles, sorts chronologically, paginates, and writes:
- Page 1 → `security-news.html`
- Page N → `security-newsN.html`

Register both generators in `get_generators()` (return a list).

Template used: `security-news` (new template below).

Context passed to template:
- `posts` — current page's security articles
- `posts_page`, `posts_paginator` — pagination objects (reuse same Pelican Paginator API)
- `title` — "Solr Security News"

---

### 2. CREATE: `themes/solr/templates/security-news.html`

Extends `subnav.html`. Subnav adds "Security News" tab alongside existing news tabs
so security-news.html feels like a sub-section of the main news area.

```jinja2
{% extends "subnav.html" %}
{% block subnav_title %}Solr™ News{% endblock %}
{% block subnav_nav_items %}
<dd><a href="{{ SITEURL }}/posts.html">All News</a></dd>
<dd><a href="{{ SITEURL }}/security-news.html" class="selected">Security News</a></dd>
<dd><a href="{{ SITEURL }}/blog.html">Blog</a></dd>
<dd><a href="{{ SITEURL }}/news.html">Announcements</a></dd>
{% endblock %}
```

Content block: same article-rendering pattern as `posts.html` but for security articles only.
Each article renders its full content inline (matching current `security.html` behavior).
Pagination links at the bottom use `security-news.html` / `security-newsN.html` URLs.

Also modify `posts.html` to add the same "Security News" tab to its subnav.

---

### 3. MODIFY: `themes/solr/templates/security.html`

- Change `[:15]` to `[:5]` in the CVE list table
- Add "See full security news history →" link below the table pointing to `security-news.html`
- Remove the full article `{% for %}` block (moves to `security-news.html`)
- Remove the "CVE reports for Apache Solr dependencies" section (moves to `security-dependency-cves.html`)

---

### 4. MODIFY: `content/pages/security.md`

Complete rewrite of the prose. Structure after rewrite:

```
[callout box] Found a new vulnerability? → mailto + link to reporting-procedure.html

## Report a New Vulnerability
Brief: what makes a valid report (auth required, supported version, repro steps, plaintext).
Link to reporting-procedure.html for full detail.

## Published CVEs Detected by Scanners
Keep current Do/Don't list. Simplify prose.
Point to security-dependency-cves.html for the full dependency CVE list and VEX download.

## More Information
- Full security news history: security-news.html
- Dependency CVE list and VEX file: security-dependency-cves.html
- Reporting procedure and email templates: security-reporting.html
- ASF security resources: https://www.apache.org/security/
```

Front matter unchanged (`URL: security.html`, `template: security`).

---

### 5. CREATE: `content/pages/security-dependency-cves.md`

Front matter:
```
Title: Solr™ CVE Reports for Dependencies
URL: security-dependency-cves.html
save_as: security-dependency-cves.html
template: security-dependency-cves
```

Content (prose only — table and download button rendered by template):
- Brief intro: what is VEX, why it exists
- How to use the VEX JSON file with scanning tools
- Invitation to join security-discuss mailing list or contact security@apache.org

---

### 6. CREATE: `themes/solr/templates/security-dependency-cves.html`

Extends `page.html`. Renders:
1. `{{ page.content }}` (VEX explanation prose)
2. A large styled download button:
   ```html
   <a href="/solr.vex.json" class="button large" download>
     Download Solr VEX File (JSON)
   </a>
   ```
3. The full CVE dependency table (moved verbatim from current `security.html`):
   - Columns: id, versions, jars, state, detail
   - Filters `vex` context for `analysis.state != "exploitable"` (same as current)

---

### 7. CREATE: `content/pages/security-reporting.md`

Front matter:
```
Title: Solr™ Vulnerability Reporting Procedure
URL: security-reporting.html
save_as: security-reporting.html
template: security-reporting
```

**Sections** (each with HTML `id` anchor for subnav):

**1. Introduction** (`id="introduction"`)

> Apache Solr is maintained by volunteers. The PMC will make every effort to respond,
> but cannot guarantee specific response times. We appreciate your patience and your
> contribution to the security of the project.
>
> If you have concerns about how the project team is handling a report, you may also
> contact [security@apache.org](mailto:security@apache.org). For PMC members, the ASF
> provides detailed [committer guidance on vulnerability handling](https://www.apache.org/security/committers.html).

**2. Submission Rules** (`id="submission-rules"`)

1. Plaintext email only — no zip files, no links to external docs, no PDFs
2. One vulnerability per email — for multiple issues, send separate emails
3. Include reproduction steps — scanner output alone is not a report
4. Test with authentication and authorization enabled — running without auth is a misconfiguration
5. Test against a supported Solr version — check solr.apache.org/downloads.html

**3. Workflow Diagram** (`id="workflow"`)

Raw HTML `<figure>` block with inline PNG image (SVG to follow):
```html
<figure>
  <img src="{filename}/images/security-vuln-process.png"
       alt="Solr vulnerability reporting workflow diagram"
       style="max-width:100%; height:auto;" />
  <figcaption>Vulnerability reporting workflow</figcaption>
</figure>
```

**4. What to Expect** (`id="what-to-expect"`)

| Step | Who | Timeframe |
|------|-----|-----------|
| Initial triage / acknowledgment | PMC volunteers | Up to 7 days |
| Full investigation | PMC volunteers | Up to 30 days |
| CVE ID request | PMC + ASF Security Team (CNA) | During fix development |
| Fix + CVE publication | PMC + ASF Security Team | Coordinated with you |
| Credit in advisory | PMC | At public disclosure |

> Public disclosure is announced on the [oss-security mailing list](https://oss-security.openwall.org/wiki/mailing-lists/oss-security)
> following the ASF standard process.

**5. Canned Email Responses** (`id="canned-responses"`)

Five `<details>/<summary>` collapsible blocks — see full content below.

**6. After Acceptance: JIRA Process** (`id="jira-process"`)

1. Create a private JIRA issue (set appropriate security level — not public)
2. Send acknowledgment email (use Response A template)
3. Issue is included in the weekly security-issues digest email
4. PMC coordinates investigation via private JIRA, security list, and security Slack
5. When fix is ready: request CVE ID from ASF Security Team via the CVE portal
6. Notify reporter of planned disclosure date
7. Publish fix release, then publish CVE advisory
8. Announce on oss-security@lists.openwall.com (handled by ASF Security Team)
9. Update security.html and close JIRA

---

### 8. CREATE: `themes/solr/templates/security-reporting.html`

```jinja2
{% extends "subnav.html" %}
{% block subnav_title %}Vulnerability Reporting Procedure{% endblock %}
{% block subnav_subtitle %}How the Solr PMC handles security disclosures{% endblock %}
{% block subnav_nav_items %}
<dd><a href="#submission-rules">Submission Rules</a></dd>
<dd><a href="#workflow">Workflow</a></dd>
<dd><a href="#what-to-expect">What to Expect</a></dd>
<dd><a href="#canned-responses">Email Templates</a></dd>
<dd><a href="#jira-process">After Acceptance</a></dd>
{% endblock %}
{% block content_inner %}
<div class="small-12 columns">{{ page.content }}</div>
{% endblock %}
```

---

### 9. PLACE: `themes/solr/static/images/security-vuln-process.png`

Copy from `~/Downloads/solr_vuln_process.png`. Referenced in the procedure page as shown
in section 7 above. A future commit replaces this with an SVG.

---

## Canned Email Responses

### A — Acknowledgment (report accepted)
**`<summary>`:** Response A: Acknowledgment — report received and under review

```
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
```

### B — Reject: scanner output, no reproduction steps
**`<summary>`:** Response B: Reject — scanner output without reproduction steps

```
Subject: Re: [Original Subject]

Thank you for contacting the Solr security team.

We are unable to process reports that consist solely of scanner tool output
without a demonstrated reproduction of the vulnerability in Apache Solr.

Scanner reports list dependency CVEs that are often not applicable to how
Solr uses those libraries. Before filing a security report, please:

1. Check https://solr.apache.org/security-dependency-cves.html — we publish a VEX file
   listing CVEs already assessed as not exploitable in Solr.
2. Verify the issue is actually exploitable in a properly configured Solr
   instance (with authentication and authorization enabled).
3. Write step-by-step reproduction steps that demonstrate the impact on
   Solr specifically.

For dependency upgrade discussions, the public Solr users list is the
right venue: users@solr.apache.org

Apache Solr Security Team
```

### C — Reject: multiple vulnerabilities in one email
**`<summary>`:** Response C: Reject — multiple distinct vulnerabilities in one email

```
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
```

### D — Reject: attachment or external link instead of plaintext
**`<summary>`:** Response D: Reject — report sent as zip file or external link

```
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
```

### E — Reject: no authentication / behavior within role
**`<summary>`:** Response E: Reject — no authentication configured or behavior within expected role

```
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
```

---

## Testing

1. `./build.sh` — no Pelican errors; verify all new output files exist:
   - `output/security.html` — rewritten, last 5 CVEs, callout box
   - `output/security-news.html` — full paginated security article history
   - `output/security-dependency-cves.html` — VEX explanation, table, download button
   - `output/security-reporting.html` — workflow diagram, canned responses
2. Check subnav anchor links resolve (`#submission-rules`, `#workflow`, etc.)
3. Verify diagram image renders and scales at 320px, 768px, 1200px viewports
4. Verify `<details>/<summary>` collapse works (no JS required)
5. Check "See full security news history" link on security.html points to security-news.html
6. Check download button on security-dependency-cves.html links to `/solr.vex.json`
7. Verify the security.html URL and top-nav link are unchanged
