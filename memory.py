import chromadb
from chromadb.utils import embedding_functions

# Use SentenceTransformers instead of OpenAI embeddings
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"   # lightweight, widely used
)

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="research_summaries",
    embedding_function=embedding_func
)

def store_summary(title, summary, link):
    collection.add(
        documents=[summary],
        metadatas=[{"title": title, "link": link}],
        ids=[title]
    )

def search_summaries(query):
    return collection.query(query_texts=[query], n_results=3)
