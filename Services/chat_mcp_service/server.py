from mcp.server.fastmcp import FastMCP

# Instantiate your server
mcp = FastMCP("HelloWorld")

# Define a simple tool that greets the user
@mcp.tool()
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Start the server (defaults to stdio transport)
    mcp.run()  # or mcp.run(transport="sse") for SSE-based hosts