# src/database.py

import sqlite3
from typing import List, Tuple, Optional
from pathlib import Path

DB_PATH = "ot_learning.db"  # 프로젝트 루트에 생성

# DB 초기화 (없으면 자동 생성)
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            question_id TEXT,
            answer TEXT,
            correct INTEGER,
            score INTEGER,
            timestamp TEXT
        )
        """)
        conn.commit()

def save_history(user_id: str, question_id: str, answer: str, correct: bool, score: int, timestamp: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO history (user_id, question_id, answer, correct, score, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, question_id, answer, int(correct), score, timestamp))
        conn.commit()

def get_user_history(user_id: str) -> List[Tuple]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT question_id, answer, correct, score, timestamp
        FROM history
        WHERE user_id = ?
        ORDER BY timestamp DESC
        """, (user_id,))
        return cursor.fetchall()

def get_user_score_summary(user_id: str) -> Tuple[int, int]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT COUNT(*), SUM(score) FROM history WHERE user_id = ?
        """, (user_id,))
        row = cursor.fetchone()
        total = row[0] or 0
        correct = row[1] or 0
        return total, correct