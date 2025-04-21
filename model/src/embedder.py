# src/embedder.py

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# 기본 모델 (변경 가능): all-MiniLM-L6-v2 또는 XLM-RoBERTa 등
DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class Embedder:
    def __init__(self, model_name: str = DEFAULT_MODEL_NAME):
        print(f"🔧 임베딩 모델 로딩 중: {model_name}")
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        여러 문장을 벡터로 변환
        :param texts: ["문장1", "문장2", ...]
        :return: [[0.11, -0.23, ...], [...]]
        """
        return self.model.encode(texts, convert_to_tensor=False, normalize_embeddings=True)

    def embed_one(self, text: str) -> List[float]:
        """
        단일 문장 벡터화
        """
        return self.embed([text])[0]

# 모듈 테스트
if __name__ == "__main__":
    embedder = Embedder()
    vec = embedder.embed_one("작업치료사의 주요 역할은 무엇인가요?")
    print(f"벡터 차원: {len(vec)}")
    print(f"예시 벡터: {vec[:5]}")