import random
from mcp.server.fastmcp.server import FastMCP

mcp: FastMCP = FastMCP("Fuzzy Calculator")


@mcp.tool("fuzzy_add")
def fuzzy_add(a: int, b: int) -> int:
    """Add two numbers, but randomly"""
    return random.randint(a, b)


if __name__ == "__main__":
    mcp.run()
