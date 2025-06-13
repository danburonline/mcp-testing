import asyncio
from fastmcp import Client, FastMCP

# Example transports (more details in Transports page)
server_instance = FastMCP(name="MCPTestServer") # In-memory server
http_url = "http://localhost:8080/mcp"        # HTTP server URL
server_script = "main.py"         # Path to a Python server file

# Client automatically infers the transport type
# client_in_memory = Client(server_instance)
client_http = Client(http_url)

# client_stdio = Client(server_script)

# print(client_in_memory.transport)
print(client_http.transport)
# print(client_stdio.transport)

# Expected Output (types may vary slightly based on environment):
# <FastMCP(server='TestServer')>
# <StreamableHttp(url='https://example.com/mcp')>
# <PythonStdioTransport(command='python', args=['/path/to/your/my_mcp_server.py'])>