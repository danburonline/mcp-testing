import asyncio
import os
from fastmcp import Client
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = Client("http://localhost:8080/mcp/")
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tools = []

    async def get_llm_response(self, prompt):
        """Get response from OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI: {str(e)}"

    async def chat(self, user_input):
        """Main chat loop using real LLM"""
        try:
            async with self.client:
                # Get available tools
                self.tools = await self.client.list_tools()
                
                # Get LLM's response
                llm_response = await self.get_llm_response(user_input)
                print(f"\n🤖 LLM Response: {llm_response}")
                
                # Use MCP tools based on LLM's response
                if llm_response and "random" in llm_response.lower():
                    print("\n🛠️ Using fuzzy_add tool")
                    result = await self.client.call_tool("fuzzy_add", {"a": 1, "b": 10})
                    return f"Here's a random number: {result}"
                else:
                    print("\n🛠️ Using ask_gpt tool")
                    result = await self.client.call_tool("ask_gpt", {
                        "prompt": user_input,
                        "model": "gpt-4o-mini"
                    })
                    return f"Here's what I found: {result}"

        except Exception as e:
            return f"Error occurred: {str(e)}"

async def main():
    llm = LLMClient()
    
    print("🤖 LLM Client is ready! Type 'quit' to exit.")
    while True:
        user_input = input("\n👤 Your question: ").strip()
        if user_input.lower() == 'quit':
            break
            
        response = await llm.chat(user_input)
        print(f"🤖 Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    asyncio.run(main()) 