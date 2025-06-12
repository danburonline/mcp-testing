# MCP Testing

Goal to teach to students LLM APIs, MCPs, etc.

## Prerequisites

### Install uv

Ensure you have uv installed. uv is a fast Python package installer and resolver.

```sh
# Install uv using Homebrew on macOS
brew install uv
```

Verify uv installation:

```sh
uv --version
```

## Environment Setup

### Create and Activate Virtual Environment

```sh
# Create a virtual environment using uv
uv venv --seed
```

## Installing all dependencies

```sh
uv pip install -r pyproject.toml
```

## Example Usage

```sh
# This will run the Python script with the Python version installed inside the virtua lenvironment
uv run example.py
```
