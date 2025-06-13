#!/bin/bash

# Function to cleanup on exit
cleanup() {
  echo ""
  echo "Client execution completed."
  exit 0
}

# Set up trap to handle interrupts
trap cleanup SIGINT SIGTERM

# Check if server is running
echo "Checking if MCP server is accessible..."
if ! curl -s http://localhost:8080/mcp >/dev/null 2>&1; then
  echo "Warning: MCP server doesn't appear to be running on localhost:8080"
  echo "Please make sure to start the server first using: ./scripts/server.sh"
  echo "Continuing anyway..."
fi

# Run the MCP client
echo "Starting MCP client..."
uv run src/client/main.py

echo "Client execution finished."
