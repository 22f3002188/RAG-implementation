from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
import os, shutil

from ingestion.loader import load_files
from ingestion.chunker import chunk_documents
from retrieval.vector_store import build_vector_store
from retrieval.retriever import retrieve
from generation.generator import generate_test_cases
from guards.safety import check_minimum_evidence   # ✅ SAFETY IMPORT

app = FastAPI()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------------
# Serve UI
# -------------------------------
@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("ui/index.html", "r", encoding="utf-8") as f:
        return f.read()

# -------------------------------
# UI-based generation endpoint
# -------------------------------
@app.post("/ui-generate")
def ui_generate(
    files: list[UploadFile] = File(...),
    query: str = Form(...)
):
    # 1️⃣ Save uploaded files
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    # 2️⃣ Load documents
    docs = load_files(UPLOAD_DIR)
    if not docs:
        return {
            "error": "No readable text found in uploaded files."
        }

    # 3️⃣ Chunk documents
    chunks = chunk_documents(docs)
    if not chunks:
        return {
            "error": "Files loaded but no usable text chunks were created."
        }

    # 4️⃣ Build vector store
    vectorstore = build_vector_store(chunks)

    # 5️⃣ Retrieve relevant chunks
    retrieved_chunks = retrieve(vectorstore, query, top_k=5)

    # 6️⃣ SAFETY CHECK (VERY IMPORTANT)
    if not check_minimum_evidence(retrieved_chunks):
        return {
            "error": "Insufficient context to generate a reliable answer. Please upload more relevant documents."
        }

    # 7️⃣ Build context
    context = "\n".join(chunk.page_content for chunk in retrieved_chunks)

    # 8️⃣ Generate answer using LLM
    answer = generate_test_cases(context, query)

    # 9️⃣ Return response
    return {
        "query": query,
        "response": answer
    }
