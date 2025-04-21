# jjw - 04.21~04.22

## 작업치료사 국가고시 문제를 기반으로 한 맞춤형 학습 챗봇 시스템  

---

### 0. 목표는 동일
> 사용자가 로그인   
> 맞춤형 문제를 추천   
> 답안을 제출   
> AI가 채점   
> 이력과 오답노트를 관리   

--- 

### 1. API 기반 프로젝트 (OpenAI 또는 외부 API 호출)   
- 모델: OpenAI API (GPT-4 등)   
- 처리방식: FastAPI 서버 구축 -> 외부 API 호출 -> 응답 반환   
- 입력: PDF 로부터 문제 추출 -> DB 저장 또는 임베딩   
- UI: Streamlit 기반 인터페이스로 로그인, 문제 추천, 채첨    
- AI 기능: AI 응답을 받아 채점 + 해설 생성 (개발중)   
- 주요 도구: FastAPI, requests, OpenAI, Chroma, LangChain, Streamlit   
- 구성: [app.py](/api/app.py), [vector_store.py](/api/pdf_loader/vector_store.py), [embedder.py](/api/pdf_loader/embedder.py), [app.py](/api/pdf_loader/loader.py)   
- 장점: 설정 간단, 코드 간단, 서버만 잘 돌면 안정적   
- 단점: OpenAI 요금 발생, API 속도 지연, 수정 제약, 프롬프트만 수정 가능   

--- 

### 2. 허깅페이스 기반 프로젝트 (로컬 LLM 실행)   
- 모델: Hugging Face 모델 (Exaone  3.5 7.8B)      
- 처리방식: ollama run exaone3.5:7.8b로 로컬 모델 구동     
- 입력: PDF 문제 로딩 -> 벡터 임베딩 + DB 저장   
- UI: Streamlit 기반 인터페이스로 로그인, 문제 추천, 채첨, 리포트 제공, 오답노트   
- AI 기능: 로컬에서 실행되는 모델이 직접 해설 제공   
- 주요 도구: sentence-transformers, ChromaDB, Streamlit, SQLite   
- 구성: [app.py](/model/app.py), [database.py](/model/src/database.py), [embedder.py](/model/src/embedder.py), [llm_runner.py](/model/src/llm_runner.py), [pdf_loader.py](/model/src/pdf_loader.py), [question_selector.py](/model/src/question_selector.py), [scorer.py](/model/src/scorer.py), [user_manager.py](/model/src/user_manager.py), [utils.py](/model/src/utils.py), [vector_store.py](/model/src/vector_store.py)  
- 장점: 오프라인 실행 가능, 속도 빠름, 완전한 제어권, 수정 모든지 가능   
- 단점: 사양 요구 높음 (RAM/GPU), 초기 설정 복잡

--- 

### 3. 정리
> 빠르게 결과, 클라우드 기반 -> API 기반 구축   
> LLM을 커스터마이징하고, 로컬에서 운영 -> Model 구축
