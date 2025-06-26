# 電商智能代理平台

## 專案簡介
一個以 Python 打造的現代化電商平台，結合多智能體（Multi-Agent）與進階檢索增強生成（RAG）技術，支援多模態輸入、持續對話、工具協作與串流回應，並內建小型文件庫。

### 專案概述
本平台旨在展示如何運用 AI Agent 技術提升電商體驗，包含商品推薦、客服問答、知識檢索等多元應用。系統設計強調模組化、可擴展性與多工具協作，適合教學、研究或原型開發。

## 主要功能
- 多智能體（Multi-Agent）協作
- 進階 RAG（檢索增強生成）
- 持續對話記憶（可追溯上下文）
- 多模態支援（文字、圖片等）
- 工具間資料互用
- 串流回應（Streaming）
- 內建小型文件庫（可自訂文件）

## 技術棧
- Python 3.10+
- FastAPI（API 與串流）
- LangChain / LlamaIndex（RAG 與 Agent 框架）
- SentenceTransformers / FAISS（向量檢索）
- OpenAI / HuggingFace Transformers（LLM 與多模態）
- WebSocket（即時串流）
- SQLite / JSON（文件庫儲存）

## 安裝與建置
1. 下載或 clone 此專案：
   ```bash
   git clone <repo_url>
   cd E-commerce_Agent
   ```
2. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```
3. 啟動服務：
   ```bash
   uvicorn app.main:app --reload
   ```

## 使用說明
- API 文件可於 http://localhost:8000/docs 查看
- 可透過 `/chat` 端點進行多輪對話與多模態互動
- 文件庫可於 `docs/` 目錄自訂與擴充

## 最新變更
- 2024-06-27：專案初始化，建立 README 與基本規劃

## 貢獻方式
歡迎提交 issue 或 pull request 改善本專案。

## 授權條款
本專案採用 MIT License。

This project is licensed under the [MIT License](./LICENSE).