# parsing/parse_pdfs.py
import fitz  # PyMuPDF
import os

def parse_all_pdfs(folder_path):
    pdf_texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            with fitz.open(full_path) as doc:
                text = "".join(page.get_text() for page in doc)
                pdf_texts[filename] = text
    return pdf_texts
