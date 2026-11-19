Title: Apache Solr and Java4Shell (CVE-2026-114938)
category: solr/news
save_as:

*From the Apache Solr PMC*

A critical OpenJDK RCE vulnerability, CVE-2026-114938 ("Java4Shell"), was disclosed on November 17, 2026. It is a vulnerability in the Java runtime (OpenJDK), **not in Apache Solr** - but Solr was publicly named as an application where exploitation was demonstrated, so users should act.

**The fix is to update your JDK.** No Solr release addresses this, because the bug is not in Solr.

### Does it affect my Solr?

Your deployment is affected only if **ALL three** conditions are met:

1. The JDK is OpenJDK 17.0.6 or later (Temurin, Corretto, Zulu, Red Hat, Oracle, etc.).
2. The CPU is x86-64 with AVX-512 VBMI (Intel Ice Lake / Sapphire Rapids / Emerald Rapids / Granite Rapids; AMD Zen 4+). ARM/Apple Silicon is not affected. To check on Linux: `grep -o 'avx512vbmi' /proc/cpuinfo`
3. A reachable path decodes attacker-controlled Base64. If you are unsure of the answer to this, assume that such a path exists.

### What to do

1. **Update your JDK** to a patched build (Oracle Nov 2026 CPU / OpenJDK 2026-11-17 advisory). Patched builds end in `.1`:
    * Java 17 → 17.0.21.1
    * Java 21 → 21.0.13.1
    * Java 25 → 25.0.5.1
    * Java 27 → 27.0.1.1
2. **Restart every Solr node** after patching - a running JVM stays vulnerable until restarted.
3. **If you can't patch yet**, start the JVM with `-XX:-UseBASE64Intrinsics` or `-XX:UseAVX=2` (x86-64 only). Do **not** use `-XX:DisableIntrinsic=_base64_decodeBlock` alone - it can break JVM startup.

### Official Solr container images

If you run Solr using our [official container images](https://hub.docker.com/_/solr):

* Make sure you're on a [supported tag](https://hub.docker.com/_/solr). If you're not, upgrade.
* Supported images are rebuilt regularly with the latest JRE and Linux patches and published under the same tags.
* **Patched images are not available yet.** The Solr images are built on Eclipse Temurin, and a rebuilt Solr image can only be published once patched Temurin base images are released. That may take anywhere from hours to days.
* **Don't wait for the new image. Apply the JVM flag now.** Set `SOLR_OPTS="-XX:-UseBASE64Intrinsics"` on your current containers (e.g. `docker run -e SOLR_OPTS="-XX:-UseBASE64Intrinsics" …`) and recreate them. This protects you on the image you're already running.
* **Once the patched image is published**, re-pull it and recreate your containers. This won't happen on its own for images you're already running. If you pin by digest (`solr@sha256:…`), switch to the new digest once you've confirmed it has the patched Java. After that you can remove the JVM flag.
* To check which Java version you have, look at the JVM section of the Solr Admin UI dashboard, or run `docker run --rm solr:<tag> java -version`. It should show one of the patched versions listed above (e.g. 17.0.21.1, 21.0.13.1) or later.

### Bottom line

Updating your JDK is the fix, and we strongly recommend doing it as soon as a patched build is available for your platform. Until then, the JVM flags above are a safe, effective way to protect your deployment today. Don't rely on authentication or network isolation alone to cover this issue. Patch the JDK or apply the flag.

### References

* OpenJDK advisory: <https://openjdk.org/groups/vulnerability/advisories/2026-11-17>
* Oracle CPU: <https://www.oracle.com/security-alerts/cspunov2026.html>
* CISA alert: <https://www.cisa.gov/news-events/alerts/2026/11/17/critical-java-vulnerability-requires-immediate-patching>
* Disclosure (Calif): <https://calif.io/java4shell>

The PMC is monitoring this and will update as needed. Questions can be sent to [users@solr.apache.org](mailto:users@solr.apache.org) or, for security-sensitive matters, [security@solr.apache.org](mailto:security@solr.apache.org).
