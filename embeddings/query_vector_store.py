from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")

def query_vector_store(query, top_k=5, persist_path="chroma_db", return_docs=False):
    chroma_client = chromadb.PersistentClient(path=persist_path)
    collection = chroma_client.get_or_create_collection(name="offer_docs")

    query_embedding = model.encode(query).tolist()

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

