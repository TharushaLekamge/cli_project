from mcp.server.fastmcp import FastMCP

from prompts import register_prompts
from resources import register_resources
from tools import register_tools

mcp = FastMCP("DocumentMCP", log_level="ERROR")

register_tools(mcp)
register_resources(mcp)
register_prompts(mcp)


if __name__ == "__main__":
    mcp.run(transport="stdio")
