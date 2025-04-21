# app.py (수정됨)
import streamlit as st
import re
import matplotlib
matplotlib.rcParams['font.family'] = 'AppleGothic'  # macOS 한글 폰트 설정
matplotlib.rcParams['axes.unicode_minus'] = False

from src.pdf_loader import load_pdf_questions
from src.vector_store import store_documents, search_similar
from src.llm_runner import generate_response
from src.scorer import evaluate_answer, extract_correctness_from_response
from src.user_manager import login, get_username
from src.question_selector import load_questions, select_question
from src.database import init_db, save_history, get_user_history
from src.utils import get_timestamp, format_datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

# 초기 설정
init_db()
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# 로그인 화면
if st.session_state.user_id is None:
    st.title("🧠 작업치료사 국가고시 학습 챗봇")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        try:
            user_id = login(username, password)
            st.session_state.user_id = user_id
            st.success(f"환영합니다, {username}님!")
        except ValueError:
            st.error("로그인 실패. 비밀번호를 확인하세요.")
    st.stop()

# 사용자 정보
user_id = st.session_state.user_id
username = get_username(user_id)
st.sidebar.write(f"**로그인됨:** {username}")

# 문제 불러오기 (PDF 기반, 최초 1회)
if "questions_loaded" not in st.session_state:
    questions = load_pdf_questions("/Users/gabriel/Desktop/jjw/model/data/2.pdf")
    for i, q in enumerate(questions):
        q["id"] = f"q{i+1}"
        q.setdefault("concept", "일반")
    st.session_state.questions = questions
    load_questions(questions)
    store_documents([{"id": q["id"], "content": q["content"]} for q in questions])
    st.session_state.questions_loaded = True

questions = st.session_state.get("questions", [])

# 기능 선택
st.sidebar.title("📚 기능 선택")
mode = st.sidebar.radio("모드를 선택하세요", ["문제 풀기", "개념별 학습 리포트", "오답 노트"])

if mode == "문제 풀기":
    st.header("📋 문제 풀기")
    difficulty = st.selectbox("난이도 선택", ["하", "중", "상"])
    concepts = ["전체"] + [q["concept"] for q in questions]
    concept = st.selectbox("개념 선택", sorted(set(concepts)))

    if st.button("문제 추천받기"):
        selected = select_question(
            difficulty=difficulty,
            concept=None if concept == "전체" else concept
        )
        if selected:
            st.session_state.current_question = selected
            st.session_state.ai_response = None
        else:
            st.warning("조건에 맞는 문제가 없습니다.")

    if "current_question" in st.session_state:
        q = st.session_state.current_question
        st.subheader("문제")

        # 보기 정리
        content_lines = q['content'].split("\n")
        question_line = content_lines[0]
        choices = [line for line in content_lines[1:] if re.match(r"^[A-D]\.", line)]

        st.markdown(f"**{question_line}**")
        for choice in choices:
            st.markdown(f"- {choice}")

        user_answer = st.radio("당신의 선택은?", options=["A", "B", "C", "D"], horizontal=True)

        if st.button("채점하기"):
            docs = search_similar(q['content'], top_k=2)
            ai_feedback = generate_response(q['content'], docs)
            is_correct = extract_correctness_from_response(user_answer, ai_feedback)
            result = {
                "correct": is_correct,
                "score": 1 if is_correct else 0,
                "feedback": "정답입니다! 🎉" if is_correct else "틀렸습니다."
            }

            st.markdown(f"### ✅ 결과: {'정답' if result['correct'] else '오답'}")
            st.write(result["feedback"])
            st.markdown("---")
            st.markdown("### 🤖 AI 해설")
            st.write(ai_feedback)

            save_history(
                user_id=user_id,
                question_id=q["id"],
                answer=user_answer,
                correct=result["correct"],
                score=result["score"],
                timestamp=format_datetime(get_timestamp())
            )
            st.session_state.ai_response = ai_feedback

elif mode == "개념별 학습 리포트":
    st.header("📊 개념별 학습 리포트")
    records = get_user_history(user_id)
    if not records:
        st.info("아직 풀이 기록이 없습니다.")
    else:
        concept_map = {q["id"]: q.get("concept", "일반") for q in questions}
        data = []
        for r in records:
            qid = r[0]
            concept = concept_map.get(qid, "기타")
            data.append({"개념": concept, "정답여부": r[2]})

        df = pd.DataFrame(data)
        concept_summary = df.groupby("개념")["정답여부"].agg(["count", "sum"])
        concept_summary["정답률"] = concept_summary["sum"] / concept_summary["count"] * 100

        st.dataframe(concept_summary.reset_index())

        st.subheader("📈 개념별 정답률 시각화")
        fig, ax = plt.subplots()
        concept_summary["정답률"].plot(kind="bar", ax=ax, color="skyblue")
        ax.set_ylabel("정답률 (%)")
        ax.set_xlabel("개념")
        ax.set_title("개념별 정답률")
        st.pyplot(fig)

elif mode == "오답 노트":
    st.header("❌ 오답 노트")
    records = get_user_history(user_id)
    wrongs = [r for r in records if r[2] == 0]
    concept_map = {q["id"]: q.get("concept", "기타") for q in questions}
    question_map = {q["id"]: q.get("content", "") for q in questions}
    answer_map = {q["id"]: q.get("answer", "?") for q in questions}

    if not wrongs:
        st.success("푼 문제 중 오답이 없습니다!")
    else:
        for r in wrongs:
            qid = r[0]
            user_ans = r[1]
            date = r[4]
            concept = concept_map.get(qid, "?")
            question_text = question_map.get(qid, "(문제 없음)")
            correct_answer = answer_map.get(qid, "?")

            st.markdown(f"""
            ### ❌ 문제 ID: `{qid}`
            - 📘 개념: **{concept}**
            - 🕒 풀이 일시: {date}
            - 📄 문제:
              > {question_text}
            - 🙋 사용자 답: `{user_ans}`
            - ✅ 정답: `{correct_answer}`
            """)
            
            if st.button("다시 풀기", key=f"retry_{qid}_{user_ans}_{date}"):
                st.session_state.current_question = {
                    "id": qid,
                    "content": question_text,
                    "concept": concept,
                    "answer": correct_answer
                }
                st.session_state.mode = "문제 풀기"
