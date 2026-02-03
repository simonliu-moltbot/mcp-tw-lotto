# 🎰 台灣樂透助手 (mcp-tw-lotto)

這是一個基於 **FastMCP** 框架開發的 Model Context Protocol (MCP) 伺服器，支援查詢台灣大樂透與威力彩的最新開獎號碼。

## ✨ 特點
- **雙傳輸模式**：同時支援 `stdio` (本機) 與 `streamable-http` (遠端/Docker) 模式。
- **即時號碼**：同步最新開獎結果。

---

## 🚀 傳輸模式 (Transport Modes)

### 1. 本機模式 (STDIO) - 預設
適合與 Claude Desktop 搭配使用。
```bash
python src/server.py --mode stdio
```

### 2. 遠端模式 (HTTP)
適合 Docker 部署與遠端存取。
```bash
python src/server.py --mode http --port 8000
```
- **服務 URL**: `http://localhost:8000/mcp`

---

## 🔌 客戶端配置範例

### Claude Desktop (STDIO)
```json
{
  "mcpServers": {
    "tw-lotto": {
      "command": "python",
      "args": ["/絕對路徑/src/server.py", "--mode", "stdio"]
    }
  }
}
```

### Dive / HTTP 客戶端
- **Type**: `streamable`
- **URL**: `http://localhost:8000/mcp`
