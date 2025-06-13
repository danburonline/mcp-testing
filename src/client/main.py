import asyncio
import os
from fastmcp import Client
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class MCPClient:
    def __init__(self):
        self.client = Client("http://localhost:8080/mcp/")
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tools = []

    async def get_llm_response(self, prompt):
        """Get response from OpenAI to understand user intent"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. The user will ask you questions and you should provide thoughtful responses. You have access to additional tools if needed.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI: {str(e)}"

    async def get_enhanced_response(self, original_prompt, tool_response):
        """Get enhanced response from OpenAI using the tool's response"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant. You will be given a user's original question and web search results from a search tool. Your job is to analyze the search results and provide a comprehensive, well-structured answer to the user's question. You can synthesize information from multiple sources, add context, clarify points, provide additional insights, or reorganize the information to be more helpful. Present the information in a clear, engaging way that directly addresses the user's question.",
                    },
                    {
                        "role": "user",
                        "content": f"Original question: {original_prompt}\n\nTool's response: {tool_response}\n\nPlease provide an enhanced, improved response to the original question using the tool's information as a foundation.",
                    },
                ],
                max_tokens=1500,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI enhancement: {str(e)}"

    async def chat(self, user_input):
        """Process user input using MCP tools first, then enhance with LLM"""
        try:
            async with self.client:
                # Get available tools
                self.tools = await self.client.list_tools()
                print(f"📋 Found {len(self.tools)} available tools")

                print("\n" + "─" * 60)
                print("🌐 STEP 1: Calling MCP 'search_the_web' tool...")
                print("─" * 60)
                tool_result = await self.client.call_tool(
                    "search_the_web", {"query": user_input, "max_results": 3}
                )
                print(f"🔍 SEARCH RESULTS: {tool_result}")

                print("\n" + "─" * 60)
                print("🤖 STEP 2: CLIENT LLM enhancing the search results...")
                print("─" * 60)
                enhanced_response = await self.get_enhanced_response(
                    user_input, tool_result
                )
                print(f"✨ ENHANCED RESPONSE: {enhanced_response}")

                print("\n" + "═" * 60)
                print("📋 FINAL SUMMARY")
                print("═" * 60)

                final_response = f"""
┌─ 🌐 ORIGINAL SEARCH RESULTS (search_the_web via MCP server):
│  {tool_result}
│
├─ ✨ ENHANCED CLIENT RESPONSE (Client LLM improved the search results):
│  {enhanced_response}
│
└─ 💡 WORKFLOW EXPLANATION:
   • First: MCP 'search_the_web' tool searched for relevant information
   • Then: Client LLM took those results and enhanced them
   • Result: A more comprehensive and contextualized answer
"""
                return final_response

        except Exception as e:
            return f"❌ Error occurred: {str(e)}"


async def main():
    mcp_client = MCPClient()

    print("🚀 MCP Client with LLM is ready!")
    print(
        "💡 This client uses OpenAI to process your input and the search_the_web tool for enhanced responses"
    )
    print("📝 Type 'quit' to exit.\n")

    while True:
        user_input = input("👤 Your question: ").strip()
        if user_input.lower() == "quit":
            print("👋 Goodbye!")
            break

        if not user_input:
            print("⚠️ Please enter a question.")
            continue

        print("\n" + "=" * 60)
        response = await mcp_client.chat(user_input)
        print(response)
        print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
