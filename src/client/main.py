import asyncio
from fastmcp import Client

client: Client = Client("http://localhost:8080/mcp/")


async def main():
    try:
        async with client:
            tools = await client.list_tools()
            print(f"\nFound {len(tools)} available tools:")

            for tool in tools:
                print("Showing tool details:")
                print(f"- {tool.name}: {tool.description}")

            result = await client.call_tool(
                "ask_gpt",
                {
                    "prompt": "What is the capital of Switzerland?",
                },
            )
            print(f"GPT response: {result}")

        print("\nConnection closed successfully")

    except Exception as e:
        print(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
