import streamlit as st
from dotenv import load_dotenv
import os
from pdf_loader.loader import parse_pdf_questions

# Load API key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load questions from PDF
questions = parse_pdf_questions("data/2.pdf")

# 1. 로그인 화면
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Initialize session state variables safely
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current" not in st.session_state:
    st.session_state.current = 0
if "correct" not in st.session_state:
    st.session_state.correct = 0
if "incorrect" not in st.session_state:
    st.session_state.incorrect = 0
if "results" not in st.session_state:
    st.session_state.results = []
if "questions" not in st.session_state:
    st.session_state.questions = []

if not st.session_state.logged_in:
    st.title("AI 국가고시 학습 시스템")
    user = st.text_input("아이디")
    pw = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if user == "1234" and pw == "1234":
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("로그인 성공!")
        else:
            st.error("아이디 또는 비밀번호가 틀렸습니다.")
    if not st.session_state.logged_in:
        st.stop()
else:
    # 로그인 후 보여질 화면 (과목/난이도 선택)
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if not st.session_state.quiz_started:
        st.header("국가고시 시험 풀기")
        subject = st.selectbox("과목 선택", ["작업치료사", "빅데이터과"])
        st.session_state.difficulty = st.selectbox("난이도 선택", ["하", "중", "상"], key="diff_select")
        if st.button("시험 시작"):
            st.session_state.quiz_started = True
            st.session_state.subject = subject
            
            if "current" not in st.session_state:
                st.session_state.current = 0
            if "correct" not in st.session_state:
                st.session_state.correct = 0
            if "incorrect" not in st.session_state:
                st.session_state.incorrect = 0
            if "results" not in st.session_state:
                st.session_state.results = []
            if "questions" not in st.session_state:
                st.session_state.questions = []
                
            st.session_state.questions = [q for q in questions if q['difficulty'] == st.session_state.difficulty]
            st.session_state.current = 0
            st.session_state.correct = 0
            st.session_state.incorrect = 0
            st.session_state.results = []
        st.stop()

# 3. 문제풀이 (객관식)
if st.session_state.current < len(st.session_state.questions):
    q = st.session_state.questions[st.session_state.current]
    st.markdown(f"**문제 {st.session_state.current+1}: {q['question']}**")
    answer = st.radio("선택지:", q['options'])
    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False
        st.session_state.user_answer = None
        st.session_state.awaiting_understanding = False

    if not st.session_state.answer_submitted:
        if st.button("제출"):
            st.session_state.answer_submitted = True
            st.session_state.user_answer = answer
            if answer == q['answer']:
                st.session_state.feedback = ("success", "정답입니다! 👍", q['explanation'])
                st.session_state.correct += 1
            else:
                st.session_state.feedback = ("error", f"틀렸어요! 정답은: {q['answer']}", q['explanation'])
                st.session_state.incorrect += 1
            st.session_state.results.append({
                "question": q['question'],
                "selected": answer,
                "correct": q['answer'],
                "explanation": q['explanation']
            })
            st.session_state.awaiting_understanding = True
    else:
        feedback_type, feedback_msg, explanation = st.session_state.feedback
        getattr(st, feedback_type)(feedback_msg)
        st.markdown(f"**해설:** {explanation}")

        if st.session_state.awaiting_understanding:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("이해됐어요"):
                    st.session_state.current += 1
                    st.session_state.answer_submitted = False
                    st.session_state.awaiting_understanding = False
            with col2:
                if st.button("이해 안됐어요"):
                    st.info("추가 설명: 예시 상황을 들어보면 더 쉽게 이해할 수 있어요. 다음에도 다시 나올 수 있으니 꼭 복습해보세요!")
else:
    st.header("퀴즈 종료")
    st.write(f"총 {len(st.session_state.questions)}문제 중 {st.session_state.correct}개 정답, {st.session_state.incorrect}개 오답입니다.")
    for result in st.session_state.results:
        st.markdown(f"**Q:** {result['question']}")
        st.markdown(f"- 선택한 답: {result['selected']}")
        st.markdown(f"- 정답: {result['correct']}")
        st.markdown(f"- 해설: {result['explanation']}")
        st.markdown("---")

    st.button("다시 풀기", on_click=lambda: st.session_state.update(quiz_started=False, current=0, correct=0, incorrect=0, results=[]))