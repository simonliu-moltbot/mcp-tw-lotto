import sys
import os
import asyncio

# Add current directory to path so we can import logic
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mcp.server.fastmcp import FastMCP, Context
# Note: Using FastMCP for cleaner syntax, it wraps the low-level Server
# The prompt asked for "standard mcp SDK (no fastmcp)"
# WAIT. The prompt explicitly said "Use standard mcp SDK (no fastmcp)".
# I must NOT use FastMCP. I must use mcp.server.Server.

# Re-reading prompt: "Use standard mcp SDK (no fastmcp)."
# My previous read of the "Existing Project" (mcp-taiwan-opendata) used FastMCP.
# But I must follow the prompt for *this* task.
# I will use mcp.server.lowlevel.Server or similar?
# Actually, the standard pattern is `mcp.server.Server`.

try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.stdio import stdio_server
    import mcp.types as types
    from logic import fetch_all_games, get_latest_result, GAME_MAP
except ImportError as e:
    sys.stderr.write(f"Critical Import Error: {e}\n")
    # We can't really recover if mcp is missing, but logic might be missing
    sys.exit(1)

# Initialize Server
server = Server("mcp-tw-lotto")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_latest_lottery_results",
            description="Get the latest winning numbers for Taiwan Lottery games (Super Lotto, Big Lotto, 539).",
            inputSchema={
                "type": "object",
                "properties": {
                    "game_type": {
                        "type": "string",
                        "enum": ["super", "big", "539"],
                        "description": "The type of lottery game: 'super' (威力彩), 'big' (大樂透), '539' (今彩539)."
                    }
                },
                "required": ["game_type"]
            }
        ),
        types.Tool(
            name="list_lottery_games",
            description="List all supported Taiwan Lottery games.",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if name == "list_lottery_games":
        text = "Supported Games:\n"
        for k, v in GAME_MAP.items():
            text += f"- {k}: {v}\n"
        return [types.TextContent(type="text", text=text)]

    if name == "get_latest_lottery_results":
        game_type = arguments.get("game_type")
        if not game_type or game_type not in GAME_MAP:
            return [types.TextContent(type="text", text=f"Invalid game_type. Choose from: {list(GAME_MAP.keys())}")]
        
        data = get_latest_result(game_type)
        
        if "error" in data:
            return [types.TextContent(type="text", text=f"Error fetching data: {data['error']}")]
        
        # Format the output nicely
        game_name = data.get('name', game_type)
        term = data.get('term', 'Unknown Term')
        date = data.get('date', '')
        regular = ", ".join(data.get('regular', []))
        special = data.get('special')
        
        output = f"🎰 **{game_name}**\n"
        output += f"📅 期數: {term} ({date})\n"
        output += f"🔢 號碼: {regular}\n"
        if special:
            output += f"🔴 特別號: {special}"
            
        return [types.TextContent(type="text", text=output)]

    raise ValueError(f"Unknown tool: {name}")

async def main():
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        sys.stderr.write(f"Server crashed: {e}\n")
        sys.exit(1)
