# src/vector_store.py

import chromadb
from src.embedder import Embedder
from typing import List

# 최신 방식 Chroma Persistent 클라이언트
chroma_client = chromadb.PersistentClient(path="./chroma_store")
collection = chroma_client.get_or_create_collection(name="ot_questions")

# 임베딩 엔진 초기화
embedder = Embedder()

def store_documents(docs: List[dict]):
    """
    문제 리스트를 받아서 벡터 DB에 저장
    docs: [{"id": "q1", "content": "문제내용"}, ...]
    """
    valid_docs = [doc for doc in docs if doc.get("content")]
    if not valid_docs:
        print("❗️저장할 유효한 문서가 없습니다.")
        return
    
    texts = [doc["content"] for doc in docs]
    ids = [doc["id"] for doc in docs]
    embeddings = embedder.embed(texts)

    if len (embeddings) == 0:
        print("❗️임베딩 결과가 비어 있습니다.")
        return

    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids
    )

def search_similar(query: str, top_k: int = 3) -> List[str]:
    """
    유사 문서 검색
    """
    query_vec = embedder.embed_one(query)
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=top_k
    )
    return results["documents"][0] if results["documents"] else []

def reset_collection():
    """
    벡터 DB 초기화 (테스트용)
    """
    chroma_client.delete_collection(name="ot_questions")