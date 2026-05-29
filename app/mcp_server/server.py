from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ats-tools")

@mcp.tool()
def create_candidate(data: dict):
    ...

@mcp.tool()
def update_status(id: str, status: str):
    ...

@mcp.tool()
def schedule_interview(id: str, slot: str):
    ...

@mcp.tool()
def search_candidates(skill: str):
    ...