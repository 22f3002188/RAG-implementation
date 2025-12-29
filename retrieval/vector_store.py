from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_vector_store(chunks):
    texts = [c["content"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]

    embedder = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return FAISS.from_texts(
        texts=texts,
        embedding=embedder,
        metadatas=metadatas
    )
