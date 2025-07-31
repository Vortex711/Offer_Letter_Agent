from sentence_transformers import SentenceTransformer
import chromadb
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_and_store(chunks, persist_path="chroma_db"):
    chroma_client = chromadb.Client()

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

    print(f"✅ Stored {len(chunks)} chunks in ChromaDB.")
    return collection
