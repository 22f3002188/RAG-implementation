import os
import time
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from typing import List, Optional

from ingestion.loader import load_files
from ingestion.chunker import chunk_documents
from retrieval.vector_store import build_vector_store
from retrieval.retriever import hybrid_retrieve
from generation.generator import generate_test_cases
from guards.evidence import has_sufficient_evidence
from evaluation.basic_eval import run_basic_eval   


UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()



# UI SERVE

@app.get("/", response_class=HTMLResponse)
def serve_ui():
    with open("ui/index.html", "r", encoding="utf-8") as f:
        return f.read()



# MAIN GENERATION ENDPOINT

@app.post("/ui-generate")
def ui_generate(
    files: List[UploadFile] = File(...),
    query: str = Form(...),
    debug: Optional[bool] = Form(False)   
):
    start = time.time()

    # Reset upload directory
    shutil.rmtree(UPLOAD_DIR, ignore_errors=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save uploaded files
    for file in files:
        path = os.path.join(UPLOAD_DIR, file.filename)
        with open(path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    # Ingestion
    docs = load_files(UPLOAD_DIR)
    if not docs:
        return {
            "status": "insufficient_info",
            "missing_information": ["No readable content found in uploaded files"],
            "use_cases": []
        }

    # Chunking + indexing
    chunks = chunk_documents(docs)
    vectorstore = build_vector_store(chunks)

    # Retrieval
    retrieved_chunks = hybrid_retrieve(
        vectorstore,
        chunks,
        query,
        top_k=5
    )

    # Evidence threshold guard
    if not has_sufficient_evidence(retrieved_chunks):
        return {
            "status": "insufficient_info",
            "missing_information": [
                "Insufficient relevant information in uploaded documents"
            ],
            "use_cases": []
        }

    # Build context
    context = "\n\n".join(c["content"] for c in retrieved_chunks)

    # Generation
    result = generate_test_cases(
        context=context,
        query=query
    )

    # BASIC EVALUATION (SAFE)
  
    eval_status = "not_run"

    if debug:
        try:
            run_basic_eval(result)
            eval_status = "passed"
        except AssertionError as e:
            eval_status = f"failed: {str(e)}"

    response = {
        "latency_seconds": round(time.time() - start, 2),
        "result": result
    }

    if debug:
        response["evaluation"] = eval_status
        response["retrieved_chunk_count"] = len(retrieved_chunks)

    return response
