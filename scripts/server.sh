#!/bin/bash

# Function to cleanup background processes
cleanup() {
  echo ""
  echo "Shutting down server..."
  if [ ! -z "$SERVER_PID" ]; then
    kill $SERVER_PID 2>/dev/null
    wait $SERVER_PID 2>/dev/null
  fi
  exit 0
}

# Set up trap to handle interrupts
trap cleanup SIGINT SIGTERM

# Start the MCP server
echo "Starting MCP server..."
uv run src/server/main.py &
SERVER_PID=$!

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

echo "Server running with PID $SERVER_PID. Press Ctrl+C to stop."

# Keep the server running
wait $SERVER_PID
