"""
Agent 管理模組：
- 支援多 Agent 協作
- 對話記憶管理
- 工具協作（可串接 RAG、多模態等）
"""
from typing import List, Dict

class ConversationMemory:
    """簡易對話記憶體，儲存多輪對話。"""
    def __init__(self):
        self.history = []  # [(role, message)]

    def add(self, role, message):
        self.history.append((role, message))

    def get(self, n=10):
        return self.history[-n:]

class BaseAgent:
    """基礎 Agent，負責回應訊息，可擴充多模態、RAG、工具。"""
    def __init__(self, name="AI-Agent"):
        self.name = name
        self.memory = ConversationMemory()

    def reply(self, message, context=None):
        """回應訊息，可根據 context 決策。"""
        self.memory.add("user", message)
        reply = f"[{self.name}] 收到：{message}"
        self.memory.add("ai", reply)
        return reply

class MultiAgentManager:
    """多 Agent 管理器，可協作處理任務。"""
    def __init__(self, agent_names: List[str]):
        self.agents = {n: BaseAgent(n) for n in agent_names}

    def route(self, message, agent_name=None):
        """將訊息分派給指定 Agent。"""
        if agent_name and agent_name in self.agents:
            return self.agents[agent_name].reply(message)
        # 預設給第一個 Agent
        return list(self.agents.values())[0].reply(message) 