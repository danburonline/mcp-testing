#!/bin/bash

# Parse command line arguments
MALICIOUS_MODE="false"

while [[ $# -gt 0 ]]; do
  case $1 in
  --malicious | -m)
    MALICIOUS_MODE="true"
    echo "🔴 MALICIOUS MODE ENABLED - Server will return deceptive/malicious search results"
    shift
    ;;
  --help | -h)
    echo "MCP Server Launcher"
    echo ""
    echo "Usage: $0 [options]"
    echo ""
    echo "Options:"
    echo "  --malicious, -m    Enable malicious mode (returns deceptive search results)"
    echo "  --help, -h         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                 # Normal mode"
    echo "  $0 --malicious     # Malicious mode for testing prompt injection"
    exit 0
    ;;
  *)
    echo "Unknown option $1"
    echo "Use --help for usage information"
    exit 1
    ;;
  esac
done

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

# Start the MCP server with appropriate environment variable
echo "Starting MCP server..."
if [ "$MALICIOUS_MODE" = "true" ]; then
  echo "⚠️  WARNING: Server running in MALICIOUS MODE - will return deceptive results"
  MALICIOUS_MODE=true uv run src/server/main.py &
else
  echo "✅ Server running in NORMAL MODE"
  uv run src/server/main.py &
fi

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
