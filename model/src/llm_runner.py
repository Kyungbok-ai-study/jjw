# src/llm_runner.py

import requests
from typing import List

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "exaone3.5:7.8b"  # 설치한 모델 이름

def generate_response(user_query: str, context_docs: List[str]) -> str:
    """
    사용자 질문 + 관련 문서를 바탕으로 Ollama에서 답변 생성
    """
    context = "\n\n".join(context_docs)
    prompt = f"""당신은 작업치료 국가고시 학습 도우미입니다.
다음은 관련 배경 문서입니다:\n{context}\n
이 문서를 참고하여, 아래 질문에 대해 정확하고 친절하게 답변해주세요:

질문: {user_query}
"""

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "system", "content": "너는 작업치료사 국가고시 학습 튜터야."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["message"]["content"]
    except Exception as e:
        return f"[오류] 모델 응답 실패: {e}"