# Taiwan Lottery MCP Server (mcp-tw-lotto)

A Model Context Protocol (MCP) server that provides the latest winning numbers for Taiwan's major lottery games.

## 🇹🇼 Supported Games
- **Super Lotto (威力彩)**
- **Big Lotto (大樂透)**
- **Jincai 539 (今彩539)**

## 🛠 Installation

1. **Clone the repository**
   ```bash
   git clone <repo_url>
   cd mcp-tw-lotto
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

### Claude Desktop
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "taiwan-lottery": {
      "command": "/absolute/path/to/mcp-tw-lotto/.venv/bin/python",
      "args": ["/absolute/path/to/mcp-tw-lotto/src/server.py"]
    }
  }
}
```

### Dive
1. Open Dive Settings > MCP Servers.
2. Add New Server:
   - **Type**: `stdio`
   - **Command**: `/path/to/your/venv/bin/python`
   - **Args**: `/path/to/your/src/server.py`

## 📊 Tools
- `get_latest_lottery_results(game_type)`: Fetch latest draw numbers.
- `list_lottery_games()`: List supported game codes.

## 📄 License
MIT
