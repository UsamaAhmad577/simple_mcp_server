# Add Integers MCP Server

A small [Model Context Protocol](https://modelcontextprotocol.io) (MCP) server built with the official Python SDK. It exposes three tools, logs to a file, and runs over STDIO. It is a good starting point for learning how MCP servers, tools, logging and the MCP Inspector fit together.

## Tools

| Tool | Arguments | Description |
| --- | --- | --- |
| `add` | `a: int, b: int` | Returns `a + b`. |
| `divide` | `a: int, b: int` | Returns `a / b`. Raises an error if `b` is `0`. |
| `long_process` | `steps: int` | Simulates a long-running job (0.1 s per step) and logs each step. |

## Requirements

- Python (version as set in `pyproject.toml` / `.python-version`)
- [uv](https://docs.astral.sh/uv/) (recommended package manager)
- [Node.js](https://nodejs.org) (the MCP Inspector runs through `npx`)
- `mcp[cli]` **1.x**, pinned below 2 in `requirements.txt`

> **Why the `<2` pin?** This code uses `from mcp.server.fastmcp import FastMCP`. In MCP SDK v2, `FastMCP` was renamed to `MCPServer` and that import no longer exists. See [Migrating to v2](#migrating-to-mcp-sdk-v2) if you want the newer API.

## Setup

### With uv (recommended)

```bash
uv init .
uv add "mcp[cli]>=1.2,<2"
```

### With pip

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Project structure

```
.
├── main.py            # the MCP server
├── mcp_server.log     # created automatically when the server runs
├── pyproject.toml     # project metadata and dependencies (uv)
├── requirements.txt   # dependencies for pip users
└── README.md
```

## Run and test

### Option 1: MCP Inspector via the `mcp` CLI

```bash
uv run mcp dev main.py
```

This opens the Inspector in your browser (usually `http://localhost:6274`).

1. Click **Connect**.
2. Open the **Tools** tab and click **List Tools**.
3. Pick a tool, enter arguments, and click **Run Tool**.

### Option 2: Inspector directly (useful if `mcp dev` fails on Windows)

```bash
npx @modelcontextprotocol/inspector uv run main.py
```

### Option 3: Run the server alone

```bash
uv run main.py
```

It starts and waits for MCP messages on STDIO. This is normal, so press `Ctrl+C` to stop it.

## Logging

Logs are written to `mcp_server.log` next to `main.py`, not to the console. This matters for STDIO servers: the protocol uses stdout for messages, so printing to stdout would corrupt the connection. Logging is configured before the server is created so nothing is missed.

Example entries:

```
2026-09-30 14:20:01 - __main__ - INFO - Starting MCP server...
2026-09-30 14:20:15 - __main__ - INFO - adding 2 and 3
2026-09-30 14:20:15 - __main__ - INFO - Result is 5
```

## Error handling

`divide` raises a custom `MCPError` (code 400) when `b == 0`. The SDK reports an exception inside a tool to the client as a tool error with the message text, so the client sees "division by zero not allowed". The `400` code is only part of the exception text and is not a JSON-RPC error code.

## Connect to an MCP client

For clients that use a JSON config (for example Claude Desktop), add an entry like this. Replace the path with your own project folder:

```json
{
  "mcpServers": {
    "add_integers": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\path\\to\\your\\project",
        "run",
        "main.py"
      ]
    }
  }
}
```

## Migrating to MCP SDK v2

To move to v2, change the pin to `mcp[cli]>=2,<3` and update the import and class name:

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("add_integers")
```

The `@mcp.tool()` decorators and `mcp.run(transport="stdio")` stay the same. Note that in v2, synchronous tools such as `long_process` run on a worker thread, so they no longer block other requests. Also, `ctx.info()` style logging is deprecated there, so the standard `logging` module used here remains the right choice. Full guide: https://py.sdk.modelcontextprotocol.io/v2/migration/

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `No module named 'mcp.server.fastmcp'` | You have mcp 2.x. Install `mcp[cli]<2`, or migrate as described above. |
| `mcp dev` says the CLI is missing | Install the extra: `uv add "mcp[cli]<2"`. |
| `npx` not found | Install Node.js and reopen your terminal. |
| Postman Desktop shows "install cmd.exe" | Known Postman Desktop issue on Windows. Use the MCP Inspector instead. |
| Nothing appears in the terminal | Expected. Check `mcp_server.log` instead. |

## Resources

- [MCP documentation](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)