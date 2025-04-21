# scorer.py

import re

def evaluate_answer(user_answer: str, correct_answer: str) -> dict:
    user = user_answer.strip().upper()
    correct = correct_answer.strip().upper()
    is_correct = user == correct
    return {
        "correct": is_correct,
        "score": 1 if is_correct else 0,
        "feedback": "정답입니다! 🎉" if is_correct else "틀렸습니다."
    }

def extract_correctness_from_response(user_answer: str, ai_feedback: str) -> bool:
    """
    AI 응답에서 정답이 무엇이라고 판단했는지 추출하고, 사용자 답과 비교.
    """
    user = user_answer.strip().upper()

    # "정답은 C입니다." 또는 "정답: C"에서 정답 추출 (선택지가 줄과 줄 사이에 있는 경우도 처리)
    match = re.search(r"정답[은:]*\s*([A-D])", ai_feedback)
    if match:
        ai_answer = match.group(1).strip().upper()
        print("🔍 정답 추출됨:", ai_answer)
        return user == ai_answer

    # 보조: '정답은 ~입니다' 라는 문장 전체로부터 비교
    if f"정답은 {user}" in ai_feedback:
        return True

    # fallback: 단순 정답 메시지 기준
    if "정답입니다" in ai_feedback and "틀렸습니다" not in ai_feedback:
        return True

    return False
