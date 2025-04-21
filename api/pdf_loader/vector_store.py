from pdf_loader.embedder import embed_pdf_chunks
import chromadb
from chromadb.config import Settings

def store_in_chroma(pairs, collection_name="pdf_chunks"):
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="../../storage/chroma"
    ))
    collection = client.get_or_create_collection(name=collection_name)

    for i, (chunk, embedding) in enumerate(pairs):
        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"doc_{i}"]
        )
    
    client.persist()

def process_pdf_to_chroma(pdf_path):
    pairs = embed_pdf_chunks(pdf_path)
    store_in_chroma(pairs)
