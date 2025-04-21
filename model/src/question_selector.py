# src/question_selector.py

from typing import List, Dict, Optional
import random

# 문제 저장소 예시 (실제는 DB 또는 PDF 파싱 결과일 수 있음)
questions_db: List[Dict] = []

def load_questions(questions: List[Dict]):
    """
    외부에서 파싱된 문제 리스트를 받아 저장 (전역)
    각 문제는 다음 형식이어야 함:
    {
        "id": "q1",
        "content": "뇌졸중 후 운동 장애?",
        "concept": "중추신경계",
        "difficulty": "중"
    }
    """
    global questions_db
    questions_db = questions

def select_question(difficulty: Optional[str] = None, concept: Optional[str] = None) -> Optional[Dict]:
    """
    조건(난이도, 개념)에 맞는 문제를 하나 랜덤으로 반환
    """
    candidates = questions_db

    if difficulty:
        candidates = [q for q in candidates if q.get("difficulty") == difficulty]

    if concept:
        candidates = [q for q in candidates if concept in q.get("concept", "")]

    if not candidates:
        return None

    return random.choice(candidates)

def get_all_concepts() -> List[str]:
    """
    등록된 문제들에서 중복 없이 개념 리스트 추출
    """
    concepts = list(set(q["concept"] for q in questions_db if "concept" in q))
    return sorted(concepts)