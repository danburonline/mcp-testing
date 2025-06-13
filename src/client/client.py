import asyncio
from fastmcp import Client

# Connect to the server using HTTP transport
client = Client("http://localhost:8080/mcp/")  # Note the trailing slash

async def main():
    try:
        # Now try MCP connection
        async with client:
            print(f"Client connected: {client.is_connected()}")

            # Make MCP calls within the context
            tools = await client.list_tools()
            print(f"Available tools: {tools}")

            if any(tool.name == "fuzzy_add" for tool in tools):
                result = await client.call_tool("fuzzy_add", {"a": 1, "b": 10})
                print(f"Fuzzy add result: {result}")

        print(f"Client connected: {client.is_connected()}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 