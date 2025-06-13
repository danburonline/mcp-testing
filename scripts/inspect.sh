#!/bin/bash

# Start the MCP Inspector and open with prefilled values
echo "Starting MCP Inspector with prefilled values..."
echo "Transport type: Streamable HTTP"
echo "URL: http://localhost:8080/mcp"
echo ""
echo "Opening inspector at: http://localhost:6274/?transport=streamable-http&serverUrl=http://localhost:8080/mcp"
echo ""

# Start the inspector and open the URL with query parameters
bunx @modelcontextprotocol/inspector &

# Wait a moment for the server to start
sleep 3

# Open the browser with prefilled values
if command -v open &>/dev/null; then
  # macOS
  open "http://localhost:6274/?transport=streamable-http&serverUrl=http://localhost:8080/mcp"
elif command -v xdg-open &>/dev/null; then
  # Linux
  xdg-open "http://localhost:6274/?transport=streamable-http&serverUrl=http://localhost:8080/mcp"
elif command -v start &>/dev/null; then
  # Windows
  start "http://localhost:6274/?transport=streamable-http&serverUrl=http://localhost:8080/mcp"
else
  echo "Please manually open: http://localhost:6274/?transport=streamable-http&serverUrl=http://localhost:8080/mcp"
fi

# Keep the inspector running
wait
