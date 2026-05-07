Title: JWT Authentication Plugin: blockUnknown defaulted to false despite documentation stating true
category: solr/security
cve: 

**Severity:**
Medium

**Versions Affected:**

- Apache Solr 9.0.0 through 9.10.x
- Apache Solr 10.0.0

**Description:**

The Apache Solr JWT Authentication Plugin has a configuration parameter `blockUnknown`
that controls whether anonymous (unauthenticated) requests are blocked.
Since Solr 9.0, the Reference Guide has documented this parameter as defaulting to `true`,
meaning anonymous requests would be denied unless explicitly allowed.

Due to a documentation error introduced in SOLR-13649, the actual code default has always
been `false` — the opposite of what the documentation stated. As a result, Solr nodes
using the JWT Authentication Plugin **without** an explicit `blockUnknown` setting
in `security.json` have been accepting anonymous requests, contrary to operator expectation.

Solr nodes without any AuthorizationPlugin configured may have been inadvertently exposed
to unauthenticated access by any client with network access to Solr's port.

Nodes are **not** affected if any of the following applies:

- `blockUnknown` is explicitly set to `true` in `security.json`
- An AuthorizationPlugin (e.g., `RuleBasedAuthorizationPlugin`) is configured and correctly
  denies access to unauthorized users
- Solr is not network-accessible from untrusted clients (e.g., firewall-protected)

**Mitigation:**

Users running Solr 9.0 through 9.10.x or 10.0.0 with the JWT Authentication Plugin should verify
their `security.json` configuration. To explicitly block anonymous requests, set
`blockUnknown` to `true`:

```json
{
  "authentication": {
    "class": "solr.JWTAuthPlugin",
    "blockUnknown": true
  }
}
```

This change can be applied to a running cluster via the Config API without restart:

```bash
curl -u admin:password http://localhost:8983/solr/admin/authentication \
  -H 'Content-type:application/json' \
  -d '{"set-property": {"blockUnknown": true}}'
```

**Fix:**

Starting in Solr 9.11 and Solr 10.1, the code default for `blockUnknown` will be changed
to `true`, aligning the actual behavior with the documented behavior. Operators upgrading
from 9.x or 10.0.0 who currently rely on anonymous access through the JWT plugin while
`blockUnknown` is not explicitly configured should explicitly set `blockUnknown: false`
before upgrading to avoid a disruption.

**References:**

- GitHub PR [apache/solr#4373](https://github.com/apache/solr/pull/4373) — default change for 10.1
- GitHub PR [apache/solr#4401](https://github.com/apache/solr/pull/4401) — default change for 9.11
- [JWT Authentication Plugin documentation](https://solr.apache.org/guide/solr/latest/deployment-guide/jwt-authentication-plugin.html)
