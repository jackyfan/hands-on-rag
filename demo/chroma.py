import chromadb
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="hands-on-rag")

collection.add(
    documents=[
        "这是一篇关于人工智能RAG的文章",
        "这是一篇关于农业生产的文章"
    ],
    ids=["00001", "00002"]
)
results = collection.query(
    query_texts=["查询人工智能的文章"], # Chroma will embed this for you
    n_results=1 # how many results to return
)
print(results)
