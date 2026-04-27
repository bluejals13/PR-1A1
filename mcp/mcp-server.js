import express from 'express';
import { Server } from "@modelcontextprotocol/sdk/server/index.js"; // MCP SDK import
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js"; // 요청 스키마

const app = express();
app.use(express.json());

// MCP 서버 설정
const server = new Server(
  {
    name: "local-mcp",
    version: "1.0.0"
  },
  {
    capabilities: {
      tools: {}
    }
  }
);

// tools/list 스키마 정의 (서버에 툴 목록 제공)
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "getAuthPolicy", // 툴 이름
        description: "Returns auth policy", // 툴 설명
        inputSchema: {
          type: "object",
          properties: {} // 입력 스키마
        }
      }
    ]
  };
});

// tools/call 스키마 정의 (툴 요청 처리)
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name } = request.params;

  // getAuthPolicy 툴을 처리
  if (name === "getAuthPolicy") {
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            jwt: "1h expiration",
            type: "bearer"
          })
        }
      ]
    };
  }

  // 알려지지 않은 툴 이름에 대한 오류 처리
  throw new Error(`Unknown tool: ${name}`);
});

// GET / 처리 (UI 제공)
app.get("/", (req, res) => {
  res.send(`
    <html>
      <body>
        <h1>MCP Server UI</h1>
        <form id="authPolicyForm">
          <button type="submit">Get Auth Policy</button>
        </form>
        <pre id="response"></pre>
        <script>
          document.getElementById('authPolicyForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const response = await fetch('/mcp/tools/call', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                params: { name: 'getAuthPolicy' }
              })
            });
            const data = await response.json();
            document.getElementById('response').innerText = JSON.stringify(data, null, 2);
          });
        </script>
      </body>
    </html>
  `);
});

// POST /mcp/tools/call 처리
app.post("/mcp/tools/call", async (req, res) => {
  try {
    const { name } = req.body.params;

    // 요청된 툴 이름에 대해 직접 핸들러 호출
    const response = await server.getRequestHandler("tools/call")(req.body); // 직접 핸들러 호출
    res.json(response);
  } catch (err) {
    console.error("Error handling request:", err);
    res.status(500).json({ error: err.message });
  }
});

// 서버 시작
const port = 3001;
app.listen(port, () => {
  console.log(`MCP HTTP Server running on http://localhost:${port}/mcp`);
});