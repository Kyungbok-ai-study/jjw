# src/user_manager.py

import uuid
from typing import Dict

# 임시 사용자 저장소 (로그인 세션 관리용)
USERS: Dict[str, str] = {}  # user_id -> username

def login(username: str, password: str) -> str:
    """
    간단한 로그인 함수 (임시 비밀번호 체크)
    :return: user_id
    """
    if password != "1234":
        raise ValueError("비밀번호가 틀렸습니다.")

    # UUID로 사용자 ID 생성
    user_id = f"user-{uuid.uuid4()}"
    USERS[user_id] = username
    return user_id

def get_username(user_id: str) -> str:
    """
    user_id로 username을 조회
    """
    return USERS.get(user_id, "알 수 없음")

def logout(user_id: str):
    """
    로그아웃 처리 (세션 제거)
    """
    if user_id in USERS:
        del USERS[user_id]

def is_logged_in(user_id: str) -> bool:
    """
    유저 로그인 여부 확인
    """
    return user_id in USERS