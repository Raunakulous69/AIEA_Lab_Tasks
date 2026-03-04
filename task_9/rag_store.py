from __future__ import annotations

import os
from typing import List

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


class LocalSentenceTransformerEmbeddings:
    """
    Minimal embedding wrapper compatible with LangChain vector stores.
    Uses sentence-transformers locally (no API key).
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode([text], normalize_embeddings=True)[0].tolist()


def build_vectorstore(kb_lines: list[str], persist_dir: str = "chroma_db") -> Chroma:
    # Split not strictly necessary for short facts, but keeps it scalable.
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    docs = [Document(page_content=line) for line in kb_lines]
    chunks = splitter.split_documents(docs)

    embeddings = LocalSentenceTransformerEmbeddings()

    # Clear old store if you want clean runs
    os.makedirs(persist_dir, exist_ok=True)

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir,
    )
    vectordb.persist()
    return vectordb


def retrieve_context(vectordb: Chroma, query: str, k: int = 6) -> list[str]:
    results = vectordb.similarity_search(query, k=k)
    return [d.page_content for d in results]