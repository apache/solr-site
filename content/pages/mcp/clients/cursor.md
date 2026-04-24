Title: Cursor
URL: mcp/clients/cursor.html
save_as: mcp/clients/cursor.html
template: mcp/client

[Cursor](https://cursor.sh/) supports MCP servers natively via project configuration files or the Cursor Settings UI.

***

## STDIO Mode (Recommended) ##

### Project Configuration (`.cursor/mcp.json`) ###

Create `.cursor/mcp.json` in your project root:

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

### Cursor Settings UI ###

1. Open **Cursor Settings** (gear icon or <kbd>Cmd+,</kbd> / <kbd>Ctrl+,</kbd>)
2. Navigate to **Features** > **MCP Servers**
3. Click **Add New MCP Server**
4. Enter:
    * **Name**: `solr-mcp`
    * **Type**: `command`
    * **Command**: `docker run -i --rm -e SOLR_URL=http://host.docker.internal:8983/solr/ ghcr.io/apache/solr-mcp:latest`

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

The configuration is the same for secured and unsecured HTTP. Cursor handles the MCP OAuth2 flow automatically.

See the [Cursor MCP documentation](https://docs.cursor.com/context/model-context-protocol) for the latest configuration format.
