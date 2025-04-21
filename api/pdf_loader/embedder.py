from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

def extract_chunks_from_pdf(pdf_path, chunk_size=500):
    reader = PdfReader(pdf_path)
    full_text = ""
    for page in reader.pages:
        if page.extract_text():
            full_text += page.extract_text() + "\n"
    
    # Basic line-based chunking
    lines = full_text.splitlines()
    chunks, current_chunk = [], ""
    for line in lines:
        if len(current_chunk) + len(line) < chunk_size:
            current_chunk += line.strip() + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = line.strip() + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def embed_pdf_chunks(pdf_path, model_name='all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    chunks = extract_chunks_from_pdf(pdf_path)
    embeddings = model.encode(chunks).tolist()
    return list(zip(chunks, embeddings))
