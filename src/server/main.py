import random
import os
from fastmcp.server import FastMCP
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

mcp: FastMCP = FastMCP("Custom STDIO MCP Server")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@mcp.tool("fuzzy_add")
def fuzzy_add(a: int, b: int) -> int:
    """Add two numbers, but randomly"""
    return random.randint(a, b)


@mcp.tool("ask_gpt")
def ask_gpt(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Ask GPT a question and get a response"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )
        return response.choices[0].message.content or "No response from GPT"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=8080)

