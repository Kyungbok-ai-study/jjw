# src/pdf_loader.py

import fitz  # PyMuPDF
from typing import List, Dict
import re

def load_pdf_questions(path: str) -> List[Dict]:
    """
    PDF에서 문제, 보기를 파싱하여 반환.
    포맷 예시:
    하 1. 문제 내용
    A. 보기1
    B. 보기2 ...
    정답: B
    """
    doc = fitz.open(path)
    questions = []
    current = {}
    difficulty = None
    question_text = ""

    for page in doc:
        lines = page.get_text().split("\n")
        for line in lines:
            line = line.strip()

            # 문제 시작: 예) 하 1. 다음 중 ...
            if re.match(r"^(하|중|상)\s*\d+\.", line):
                if current:
                    questions.append(current)
                    current = {}

                difficulty_match = re.match(r"^(하|중|상)", line)
                difficulty = difficulty_match.group(1) if difficulty_match else "일반"

                parts = re.split(r"\d+\.\s*", line, maxsplit=1)
                question_text = parts[1].strip() if len(parts) > 1 else ""

                current["difficulty"] = difficulty.strip()
                current["content"] = question_text
                current["choices"] = []

            # 보기 항목: A. ~ D.
            elif re.match(r"^[A-D]\.", line):
                if "content" in current:
                    current["content"] += "\n" + line

            # 정답 줄: 예) 정답: B
            elif "정답:" in line:
                answer_part = line.split("정답:")[-1].strip().upper()
                current["answer"] = answer_part

            # 기타 줄: 보기 줄의 연속 등
            elif line:
                if "content" in current:
                    current["content"] += " " + line

    if current:
        questions.append(current)

    return questions