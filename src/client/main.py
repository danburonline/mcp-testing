import asyncio
from fastmcp import Client

# Connect to the server using HTTP transport
client: Client = Client("http://localhost:8080/mcp/")


async def main():
    try:
        # print("Connecting to server...")
        async with client:
            # print(f"✓ Successfully connected to server")
            # print(f"Connection status: {client.is_connected()}")

            # List available tools
            tools = await client.list_tools()
            print(f"\nFound {len(tools)} available tools:")
            for tool in tools:
                print(f"- {tool.name}: {tool.description}")

            # Test fuzzy_add
            print("\nTesting fuzzy_add:")
            result = await client.call_tool("fuzzy_add", {"a": 1, "b": 10})
            print(f"Random number between 1 and 10: {result}")

            # Test ask_gpt
            print("\nTesting ask_gpt:")
            result = await client.call_tool(
                "ask_gpt",
                {
                    "prompt": "What is the capital of Switzerland?",
                    "model": "gpt-4o-mini",
                },
            )
            print(f"GPT response: {result}")

        print("\nConnection closed successfully")
    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
