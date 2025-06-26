"""
RAG 模組：負責載入 docs/ 目錄下的文件，建立向量索引，並提供查詢功能。
- 使用 SentenceTransformers 進行向量化
- 使用 FAISS 建立向量索引
- 提供簡易查詢介面
"""
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SimpleRAG:
    def __init__(self, docs_dir="docs", model_name="all-MiniLM-L6-v2"):
        """
        初始化 RAG，載入文件並建立向量索引。
        :param docs_dir: 文件目錄
        :param model_name: 向量模型名稱
        """
        self.docs_dir = docs_dir
        self.model = SentenceTransformer(model_name)
        self.docs = []  # (filename, content)
        self.embeddings = None
        self.index = None
        self._load_docs()
        self._build_index()

    def _load_docs(self):
        """載入所有文件內容。"""
        for fname in os.listdir(self.docs_dir):
            fpath = os.path.join(self.docs_dir, fname)
            if os.path.isfile(fpath) and fname.endswith('.txt'):
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.docs.append((fname, content))

    def _build_index(self):
        """將文件內容向量化並建立 FAISS 索引。"""
        if not self.docs:
            return
        texts = [c for _, c in self.docs]
        self.embeddings = self.model.encode(texts, show_progress_bar=False)
        dim = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings, dtype=np.float32))

    def query(self, question, top_k=2):
        """
        查詢相關文件內容。
        :param question: 查詢問題
        :param top_k: 回傳前幾名
        :return: [(filename, content, score)]
        """
        if self.index is None:
            return []
        q_emb = self.model.encode([question])
        D, I = self.index.search(np.array(q_emb, dtype=np.float32), top_k)
        results = []
        for idx, score in zip(I[0], D[0]):
            fname, content = self.docs[idx]
            results.append((fname, content, float(score)))
        return results 