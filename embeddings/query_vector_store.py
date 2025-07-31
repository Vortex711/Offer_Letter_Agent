from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Load the same model used during indexing
model = SentenceTransformer("all-MiniLM-L6-v2")

def query_vector_store(query, top_k=5, return_docs=False):
    # In-memory DuckDB backend
    chroma_client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+memory",
        persist_directory=None
    ))
    collection = chroma_client.get_or_create_collection(name="offer_docs")

    # Embed the user query
    query_embedding = model.encode(query).tolist()

    # Perform similarity search
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    if return_docs:
        return results["documents"][0]

    print(f"\n🔍 Top {top_k} results for: \"{query}\"\n")
    for i, doc in enumerate(results["documents"][0]):
        print(f"--- Result {i+1} ---")
        print(doc[:400], "\n")
