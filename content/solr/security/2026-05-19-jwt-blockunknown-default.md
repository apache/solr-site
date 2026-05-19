Title: JWT Authentication: blockUnknown default allows unauthenticated access contrary to documentation
category: solr/security
cve:

**Severity**
moderate

**Versions Affected**

- Apache Solr 9.0.0 through 9.10.1
- Apache Solr 10.0.0

**Description**

The Apache Solr JWT Authentication Plugin has a configuration parameter `blockUnknown`
that controls whether anonymous (unauthenticated) requests are blocked. The Reference Guide
has documented this as defaulting to `true` since Solr 9.0, but the code default has always
been `false`. Operators who did not explicitly set this parameter may therefore have been
unknowingly accepting anonymous requests.

**Am I Affected?**

You may be affected if **all** of the following are true:

1. You use the JWT Authentication Plugin (`solr.JWTAuthPlugin`) in `security.json`
2. Your intention is to block all unauthenticated requests
3. Your `security.json` does **not** explicitly set `"blockUnknown": true`

You are **not** affected if any of the following applies:

- `blockUnknown` is explicitly set to `true` in `security.json`
- An AuthorizationPlugin (e.g. `RuleBasedAuthorizationPlugin`) independently denies access to unauthenticated users

**Mitigation**

Check the `authentication` section of your `security.json`. If `blockUnknown` is absent, set it explicitly to `true`.

**Fix**

Future Solr 9.11 and 10.1 releases will change the code default to `true`, matching the documentation.
Explicitly setting `blockUnknown` to `true` in a current release is sufficient; upgrading is not required.

**References**

- [JWT Authentication Plugin documentation](https://solr.apache.org/guide/solr/latest/deployment-guide/jwt-authentication-plugin.html)
