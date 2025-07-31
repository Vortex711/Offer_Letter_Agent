from parsing.parse_pdfs import parse_all_pdfs
from parsing.text_splitter import chunk_documents
from embeddings.embed_and_store import embed_and_store
from embeddings.query_vector_store import query_vector_store
from agent.generate_offer_letter import generate_offer_letter

def main():
    # Step 1: Parse PDFs
    pdf_folder = "data/"
    pdf_texts = parse_all_pdfs(pdf_folder)

    # Step 2: Chunk parsed text
    chunks = chunk_documents(pdf_texts)
    print(f"\n🔹 Created {len(chunks)} chunks.")

    # Step 3: Embed and store in Chroma Cloud
    embed_and_store(chunks)

    # Step 4: Test query
    print("\n🧪 Sample query from Chroma:")
    query_vector_store("Generate offer letter for Ramesh Kumar")

    # Step 5: Generate an actual offer letter
    print("\n📝 Generating offer letter:")
    generate_offer_letter("Martha Bennett")

if __name__ == "__main__":
    main()
