# MCP Testing

Goal to teach to students LLM APIs, MCPs, etc.

## Prerequisites

### Install Bun

Ensure you have Bun installed. Bun is a fast Node.js alternative and drop-in replacement for NPM, tsc, etc.

```sh
brew install oven-sh/bun/bun
```

### Install uv

Ensure you have uv installed. uv is a fast Python package installer and resolver.

```sh
brew install uv
```

Verify uv installation:

```sh
uv --version
```

## Environment Setup

### Create and Activate Virtual Environment

```sh
uv venv
```

## Installing all dependencies

```sh
uv sync
```

## Start the MCP Server

```sh
uv run src/server/main.py
```

This will start a local HTTP server that accepts SSEs.

## Inspect the MCP Server

Run the visual [MCP Inspector](https://github.com/modelcontextprotocol/inspector) from inside the project directory:

```sh
bunx @modelcontextprotocol/inspector
```

And then in order to connect the inspector with the MCP server, fill in the following in the left-hand panel:

- Transport type: `STDIO`
- Command: `uv`
- Arguments: `run src/server/main.py`
