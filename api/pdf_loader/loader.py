from PyPDF2 import PdfReader
import re

def parse_pdf_questions(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = "\n".join([p.extract_text() for p in reader.pages if p.extract_text()])

    # Extract 하/중/상 문제 패턴 (4지선다형)
    pattern = r'(하|중|상)\s*\d+\.\s*(.+?)\n\s*A\.\s*(.+?)\n\s*B\.\s*(.+?)\n\s*C\.\s*(.+?)\n\s*D\.\s*(.+?)(?=\n[하중상]\s*\d+\.|\Z)'
    matches = re.findall(pattern, full_text, re.DOTALL)

    questions = []
    for difficulty, q, a1, a2, a3, a4 in matches:
        questions.append({
            "difficulty": difficulty.strip(),
            "question": q.strip(),
            "options": [a1.strip(), a2.strip(), a3.strip(), a4.strip()],
            "answer": a1.strip(),  # default: A is correct (수정 가능)
            "explanation": ""      # placeholder for later use
        })

    return questions
