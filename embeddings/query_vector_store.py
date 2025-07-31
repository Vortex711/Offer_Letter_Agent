from sentence_transformers import SentenceTransformer
import chromadb
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

# Load the same model used during indexing
model = SentenceTransformer("all-MiniLM-L6-v2")

def query_vector_store(query, top_k=5, return_docs=False):
    # Use Chroma Cloud
    chroma_client = chromadb.CloudClient(
        api_key=os.getenv("YOUR_API_KEY"),
        tenant=os.getenv("TENANT"),
        database=os.getenv("DATABASE")
    )

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
