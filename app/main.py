"""
主程式：啟動 FastAPI 應用，提供電商平台 API 與 Agent 服務。
- 健康檢查
- 多輪對話（支援串流）
- 整合 RAG（知識檢索）與多 Agent 協作
- 可擴充多模態、Streaming 等
"""
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio

# 匯入 RAG 與 Agent 模組
from app.rag import SimpleRAG
from app.agent import MultiAgentManager

app = FastAPI(title="電商智能代理平台")

# 初始化 RAG 與多 Agent 管理器
rag = SimpleRAG(docs_dir="docs")
agent_mgr = MultiAgentManager(agent_names=["客服AI", "商品專家AI"])

# CORS 設定，方便前端存取
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    """健康檢查端點，回傳服務狀態。"""
    return {"status": "ok"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    """
    多輪對話端點，整合 RAG 檢索與多 Agent 回應。
    輸入：{"message": "...", "agent": "(可選)"}
    回傳：AI 回覆與相關知識內容
    """
    data = await request.json()
    user_message = data.get("message", "")
    agent_name = data.get("agent")
    # 1. 先用 RAG 查詢相關知識
    rag_results = rag.query(user_message, top_k=2)
    context = "\n".join([c for _, c, _ in rag_results])
    # 2. 交給指定 Agent 回應
    reply = agent_mgr.route(f"{user_message}\n[知識補充]\n{context}", agent_name=agent_name)
    return {"reply": reply, "knowledge": rag_results}

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket 串流對話端點，支援即時多輪互動。
    """
    await websocket.accept()
    history = []  # 可擴充為 session 記憶
    try:
        while True:
            data = await websocket.receive_text()
            # 1. RAG 查詢
            rag_results = rag.query(data, top_k=2)
            context = "\n".join([c for _, c, _ in rag_results])
            # 2. 多 Agent 回應
            ai_reply = agent_mgr.route(f"{data}\n[知識補充]\n{context}")
            await websocket.send_text(ai_reply)
            history.append(("user", data))
            history.append(("ai", ai_reply))
    except Exception:
        await websocket.close()

@app.get("/")
def root():
    """首頁簡易說明。"""
    return {"msg": "歡迎使用電商智能代理平台 API"} 