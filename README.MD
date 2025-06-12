# MCP Testing

Goal to learn MCP.

## Prerequisites

### Install UV

Ensure you have UV installed. UV is a fast Python package installer and resolver.

```bash
# Install UV using Homebrew on macOS
brew install uv
```

Verify UV installation:

```bash
uv --version
```

## Environment Setup

### Create and Activate Virtual Environment

```bash
# Create a virtual environment using UV
uv venv

# Activate the virtual environment
source .venv/bin/activate
```

## Installing all dependencies

```bash
uv pip install -r pyproject.toml
```

### Deactivate Environment

When you're done working:

```bash
deactivate
```
