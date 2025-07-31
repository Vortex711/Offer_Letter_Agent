from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os

# Load your embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_and_store(chunks):
    # Use pure in-memory DuckDB (no on-disk SQLite)
    chroma_client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+memory",
        persist_directory=None
    ))

    collection = chroma_client.get_or_create_collection(name="offer_docs")

    for chunk in chunks:
        embedding = model.encode(chunk["text"]).tolist()
        collection.add(
            documents=[chunk["text"]],
            embeddings=[embedding],
            metadatas=[{
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"]
            }],
            ids=[f'{chunk["source"]}-{chunk["chunk_index"]}']
        )

    print(f"✅ Stored {len(chunks)} chunks in in-memory ChromaDB.")
    return collection
