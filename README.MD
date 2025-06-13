# MCP Testing

Educational project for learning LLM APIs, Model Context Protocol (MCP), and security concepts like tool poisoning.

## What This Does

- **MCP Server**: Provides a mock web search tool that can operate in normal or malicious mode
- **MCP Client**: Interactive terminal chat using OpenAI + MCP tools
- **Security Testing**: Demonstrates prompt injection attacks and tool poisoning vulnerabilities

## Prerequisites

- Homebrew
- OpenAI API key

## Setup

```bash
# Install dependencies
bash scripts/deps.sh

# Add your OpenAI API key to .env
echo "OPENAI_API_KEY=your_key_here" > .env
```

## Usage

### 1. Start MCP Server

```bash
# Normal mode (safe responses)
bash scripts/server.sh

# Malicious mode (prompt injection attacks)
bash scripts/server.sh -m
```

### 2. Run MCP Client

```bash
# Interactive chat session
bash scripts/client.sh
```

The client will:

1. Send your questions to the MCP server's search tool
2. Enhance responses using OpenAI
3. Log all interactions to `logs/` directory

### 3. Inspect Server (Optional)

```bash
# Visual MCP server inspection
bash scripts/inspect.sh
```

Opens browser interface to explore available tools and test them directly.

## Educational Focus

- **Normal Mode**: Learn MCP protocol basics and client-server communication
- **Malicious Mode**: Understand security vulnerabilities in LLM-tool interactions
- **Logging**: Analyze interaction patterns and response enhancement
