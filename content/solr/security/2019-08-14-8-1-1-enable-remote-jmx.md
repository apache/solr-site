Title: [ANNOUNCE] 8.1.1 and 8.2.0 users check ENABLE_REMOTE_JMX_OPTS setting
category: solr/security

    Severity: Low

    Versions Affected:
    8.1.1 and 8.2.0 for Linux

    Description:
    It has been discovered [1] that the 8.1.1 and 8.2.0 releases contain a bad default
    setting for the ENABLE_REMOTE_JMX_OPTS setting in the default solr.in.sh file
    shipping with Solr.

    Windows users and users with custom solr.in.sh files are not affected.

    If you are using the default solr.in.sh file from the affected releases, then
    JMX monitoring will be enabled and exposed on JMX_PORT (default = 18983),
    without any authentication. So if your firewalls allows inbound traffic on
    JMX_PORT, then anyone with network access to your Solr nodes will be able to
    access monitoring data exposed over JMX.

    Mitigation:
    Edit solr.in.sh, set ENABLE_REMOTE_JMX_OPTS=false and restart Solr.
    Alternatively wait for the future 8.3.0 release and upgrade.

    References:
    [1] https://issues.apache.org/jira/browse/SOLR-13647

