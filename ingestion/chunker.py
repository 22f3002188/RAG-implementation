import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    seen = set()
    chunks = []

    for doc in documents:
        splits = splitter.split_text(doc["content"])
        for s in splits:
            h = hashlib.md5(s.encode()).hexdigest()
            if h not in seen:
                seen.add(h)
                chunks.append({
                    "content": s,
                    "source": doc["source"]
                })

    return chunks
