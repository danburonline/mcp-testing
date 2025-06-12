import random
from fastmcp import FastMCP

mcp: FastMCP = FastMCP("Fuzzy Calculator")


@mcp.tool
def fuzzy_add(a: int, b: int) -> int:
    """Add two numbers, but randomly"""
    return random.randint(a, b)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="localhost", port=8080)
