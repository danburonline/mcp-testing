#!/bin/bash

# Start the MCP server
echo "Starting MCP server..."
uv run src/server/main.py &

# Wait a moment for the server to start
sleep 3

# And then open the URL in the browser
if command -v open &>/dev/null; then
  # macOS
  open "http://localhost:8080/mcp"
elif command -v xdg-open &>/dev/null; then
  # Linux
  xdg-open "http://localhost:8080/mcp"
elif command -v start &>/dev/null; then
  # Windows
  start "http://localhost:8080/mcp"
fi
