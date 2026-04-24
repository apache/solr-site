Title: JetBrains IDEs
URL: mcp/clients/jetbrains.html
save_as: mcp/clients/jetbrains.html
template: mcp/client

[JetBrains IDEs](https://www.jetbrains.com/) (IntelliJ IDEA, WebStorm, PyCharm, etc.) support MCP servers through the AI Assistant plugin.

***

## STDIO Mode (Recommended) ##

### Project Configuration (`.junie/mcp.json`) ###

Create `.junie/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "solr-mcp": {
      "command": "docker",
      "args": ["run", "-i", "--rm",
               "-e", "SOLR_URL=http://host.docker.internal:8983/solr/",
               "ghcr.io/apache/solr-mcp:latest"]
    }
  }
}
```

### IDE Settings ###

1. Open **Settings** (<kbd>Cmd+,</kbd> / <kbd>Ctrl+Alt+S</kbd>)
2. Navigate to **Tools** > **AI Assistant** > **MCP Servers**
3. Click **Add** (`+`)
4. Configure:
    * **Name**: `solr-mcp`
    * **Transport**: `STDIO`
    * **Command**: `docker`
    * **Arguments**: `run -i --rm -e SOLR_URL=http://host.docker.internal:8983/solr/ ghcr.io/apache/solr-mcp:latest`

***

## HTTP Mode ##

Start the server first (see [Running the Server](https://github.com/apache/solr-mcp#running-the-server)), then:

```json
{
  "mcpServers": {
    "solr-mcp": {
      "url": "http://localhost:8080/mcp"
    }
  }
}
```

Or in IDE Settings, select **SSE** transport and enter `http://localhost:8080/mcp` as the URL.

The configuration is the same for secured and unsecured HTTP. JetBrains IDEs handle the MCP OAuth2 flow automatically.

MCP support requires the AI Assistant plugin. See the [JetBrains MCP documentation](https://www.jetbrains.com/help/idea/model-context-protocol.html) for the latest configuration format.
