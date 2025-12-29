def hybrid_retrieve(vectorstore, chunks, query, top_k=5):
    results = vectorstore.similarity_search_with_score(query, k=top_k)

    retrieved = []
    for doc, score in results:
        retrieved.append({
            "content": doc.page_content,
            "source": doc.metadata.get("source", ""),
            "score": float(score)
        })

    return retrieved
