def retrieve(vectorstore, query, top_k=5):
    retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
    return retriever.invoke(query)
