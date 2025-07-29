from parsing.parse_pdfs import parse_all_pdfs
from parsing.text_splitter import chunk_documents
from embeddings.embed_and_store import embed_and_store
from embeddings.query_vector_store import query_vector_store
from agent.generate_offer_letter import generate_offer_letter

def main():
    pdf_folder = "data/"
    pdf_texts = parse_all_pdfs(pdf_folder)

    chunks = chunk_documents(pdf_texts)
    print(f"\n🔹 Created {len(chunks)} chunks.")

    embed_and_store(chunks)

    query_vector_store("Generate offer letter for Ramesh Kumar")

    generate_offer_letter("Martha Bennett")

if __name__ == "__main__":
    main()
