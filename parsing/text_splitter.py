# parsing/text_splitter.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(documents, chunk_size=1000, chunk_overlap=200):
    """
    Takes a dict {source_name: text} and returns a list of chunks with metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    all_chunks = []

    for source, text in documents.items():
        chunks = text_splitter.split_text(text)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": source,
                "chunk_index": i,
                "text": chunk
            })

    return all_chunks

