📄 File-Based Multimodal RAG for Use-Case / Test-Case Generation
📌 Overview

This project implements a file-based, multimodal Retrieval-Augmented Generation (RAG) system that generates high-quality, structured use cases or test cases grounded strictly in user-provided documents.

The system ingests multiple file types (text, PDFs, DOCX, images via OCR), retrieves relevant context using hybrid search, applies evidence-based guards, and generates JSON-structured outputs suitable for QA and product documentation workflows.

This project was built as part of an AI Engineer Intern Assignment, with strong emphasis on:

RAG correctness

Hallucination prevention

Modular design

Automation

Code quality

🎯 Key Capabilities

📂 Multimodal File Ingestion

Text / Markdown

PDF

DOCX

Images (PNG / JPG) via OCR

🧠 Hybrid Retrieval

Semantic search (FAISS + embeddings)

Keyword-based matching

Deduplication

🧪 Use Case / Test Case Generation

Strict JSON output

Preconditions, steps, expected results

Negative & boundary cases

🛡️ Safety & Guards

Context-only generation (no hallucinations)

Minimum evidence threshold

Prompt-injection resistance

🔍 Debug & Observability

Retrieved chunk inspection

Ingestion & retrieval logs

⚙️ Fully Automated Pipeline

No manual steps after file upload

🧱 Architecture Overview
User Files (PDF / DOCX / TXT / Images)
        ↓
File Loader + OCR
        ↓
Text Normalization
        ↓
Chunking + Deduplication
        ↓
Vector Store (FAISS)
        ↓
Hybrid Retrieval
        ↓
Evidence Guard
        ↓
LLM Generation (JSON Only)
        ↓
Evaluation & Validation

📁 Project Structure

RAG-implementation/

├── api.py       
# FastAPI orchestration layer

├── requirements.txt

├── README.md

├── ingestion/
│   ├── loader.py  
# Multimodal file loading + OCR

│   ├── normalizer.py  
# OCR layout cleanup

│   └── chunker.py    
# Chunking & deduplication

├── retrieval/
│   ├── vector_store.py  
# FAISS vector index
│   └── retriever.py    
# Hybrid retrieval logic

├── generation/
│   └── generator.py    
# Guarded LLM generation

├── guards/
│   └── evidence.py      
# Evidence threshold enforcement

├── evaluation/
│   └── basic_eval.py  
# Output validation hooks

├── utils/
│   └── llm.py         
# Centralized LLM configuration

└── ui/
    └── index.html    
# Lightweight web UI

🚀 Getting Started
1️⃣ Clone the Repository
git clone https://github.com/your-username/RAG-implementation.git
cd RAG-implementation

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Environment Variables

UPLOAD YOUR CREDENTIALS IN .env.example file

AZURE_OPENAI_ENDPOINT=your_endpoint

AZURE_OPENAI_API_KEY=your_api_key

AZURE_OPENAI_DEPLOYMENT=your_deployment_name

AZURE_OPENAI_API_VERSION=2024-02-15-preview

                 OR

"RUN IN POWERSHELL THAN RESTART YOUR POWERSHELL"

setx AZURE_OPENAI_API_KEY "PUT YOUR KEY HERE"

setx AZURE_OPENAI_API_VERSION "PUT YOUR VERSION HERE"

setx AZURE_OPENAI_ENDPOINT "PUT YOUR ENDPOINT HERE"

setx AZURE_OPENAI_DEPLOYMENT "PUT YOUR MODEL HERE"              

⚠️ The project keeps everything file-based and local. No external databases are required.

4️⃣ Run the Application
uvicorn api:app --reload


Open your browser at:

http://localhost:8000

🧪 Example Query

Input:

Create use cases for user signup


Output (JSON):

{
  "status": "success",
  "use_cases": [
    {
      "title": "User Signup with Valid Credentials",
      "preconditions": ["User is not registered"],
      "steps": ["Enter valid email", "Set password", "Submit form"],
      "expected_result": "Account created successfully",
      "negative_cases": ["Invalid email format", "Weak password"]
    }
  ]
}


If insufficient information is available, the system responds with:

{
  "status": "insufficient_info",
  "missing_information": ["Signup fields not defined"]
}

🛡️ Safety & Guardrails

❌ No feature invention

📄 Answers strictly grounded in retrieved chunks

🔒 Ignores instructions embedded inside documents

📉 Blocks LLM calls if evidence is weak

🧹 Deduplicates low-quality chunks

📊 Evaluation & Debugging

Retrieve and inspect evidence chunks

Logs for ingestion, retrieval, and generation

Basic output validation to ensure schema correctness

⚙️ Tech Stack

Backend: FastAPI

LLM: Azure OpenAI

Embeddings: OpenAI embeddings

Vector Store: FAISS

OCR: Tesseract (via pytesseract)

Parsing: PyPDF, python-docx

Frontend: HTML + Bootstrap

🧩 Design Principles

Modular & extensible

File-based (no mandatory external DB)

Guard-first RAG design

Production-oriented structure

🚧 Future Improvements

Docker support

Reranking models

Token usage & latency metrics

Source citations in output

URL ingestion support

👤 Author

Harsh Jayswal
AI Engineer Intern Candidate
