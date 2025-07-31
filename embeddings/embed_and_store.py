from sentence_transformers import SentenceTransformer
import chromadb
from dotenv import load_dotenv
import os

load_dotenv()

# Load your embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_and_store(chunks):
    # Use Chroma Cloud
    chroma_client = chromadb.CloudClient(
        api_key=os.getenv("YOUR_API_KEY"),
        tenant=os.getenv("TENANT"),
        database=os.getenv("DATABASE")
    )

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

    print(f"✅ Stored {len(chunks)} chunks in Chroma Cloud.")
    return collection
