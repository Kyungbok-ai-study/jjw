# src/utils.py

import time
import datetime
import re

def get_timestamp() -> float:
    """
    현재 UTC 타임스탬프 반환
    """
    return time.time()

def format_datetime(ts: float) -> str:
    """
    타임스탬프를 YYYY-MM-DD HH:MM:SS 형식으로 포맷
    """
    return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def clean_text(text: str) -> str:
    """
    텍스트 전처리: 공백/줄바꿈 정리, 특수문자 제거 등
    """
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def shorten(text: str, max_len: int = 100) -> str:
    """
    너무 긴 텍스트는 자르고 '...' 붙이기
    """
    return text if len(text) <= max_len else text[:max_len] + "..."

def normalize_korean(text: str) -> str:
    """
    한글 비교를 위한 정규화 (소문자화, 공백 제거 등)
    """
    return re.sub(r"\s+", "", text).lower()