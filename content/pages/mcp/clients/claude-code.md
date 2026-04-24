Title: Claude Code
URL: mcp/clients/claude-code.html
save_as: mcp/clients/claude-code.html
template: mcp/client

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) is Anthropic's CLI tool for Claude. It supports MCP servers via the `claude mcp add` command or a `.mcp.json` project file.

***

## STDIO Mode (Recommended) ##

### CLI ###

```bash
# JAR
claude mcp add --transport stdio \
    -e SOLR_URL=http://localhost:8983/solr/ \
    solr-mcp -- java -jar /absolute/path/to/solr-mcp-1.0.0-SNAPSHOT.jar

# Docker (local image — build first with ./gradlew jibDockerBuild)
claude mcp add --transport stdio solr-mcp -- \
    docker run -i --rm -e SOLR_URL=http://host.docker.internal:8983/solr/ \
    solr-mcp:latest
```

### `.mcp.json` ###

Add to your project root:

**JAR:**

```json
{
  "mcpServers": {
    "solr-mcp": {
      "type": "stdio",
      "command": "java",
      "args": ["-jar", "/absolute/path/to/solr-mcp-1.0.0-SNAPSHOT.jar"],
      "env": { "SOLR_URL": "http://localhost:8983/solr/" }
    }
  }
}
```

**Docker (local image):**

```json
{
  "mcpServers": {
    "solr-mcp": {
      "type": "stdio",
      "command": "docker",
      "args": ["run", "-i", "--rm",
               "-e", "SOLR_URL=http://host.docker.internal:8983/solr/",
               "solr-mcp:latest"]
    }
  }
}
```

***

## HTTP Mode ##

Start the server first (see [Running the Server](https://github.com/apache/solr-mcp#running-the-server)), then:

### CLI ###

```bash
claude mcp add --transport http solr-mcp http://localhost:8080/mcp
```

### `.mcp.json` ###

```json
{
  "mcpServers": {
    "solr-mcp": {
      "type": "http",
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

### Secured HTTP (OAuth2) ###

Claude Code detects the OAuth2 challenge from the server and initiates the authorization flow automatically. The configuration is the same as unsecured HTTP.

See [Security](/mcp/security.html) for server-side OAuth2 setup.
