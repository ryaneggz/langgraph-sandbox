import os
import sys
import asyncio
from typing import List
from fastmcp import FastMCP

# Add parent directory to path so we can import from tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.search import web_scrape
mcp = FastMCP("LangGraph Sandbox MCP")

@mcp.tool(description="Fetch content from a list of URLs")
def fetch_url_content(urls: List[str]) -> str:
    return web_scrape(urls)

def main():
    MCP_HOST = os.getenv("MCP_HOST", "0.0.0.0")
    MCP_PORT = os.getenv("MCP_PORT", 8050)
    mcp.run(transport="http", host=MCP_HOST, port=MCP_PORT)

if __name__ == "__main__":    
    main()