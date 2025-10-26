from PyPDF2 import PdfReader
from pathlib import Path
import os

PDF_STORAGE = Path("pdf_texts").resolve()
PDF_STORAGE.mkdir(parents=True, exist_ok=True)

async def save_pdf_text(file, document_id):
    pdf_reader = PdfReader(file.file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    
    # Save text to file for later use
    path = os.path.join(PDF_STORAGE, f"{document_id}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    
    return text

def load_pdf_text(document_id):
    path = PDF_STORAGE / f"{document_id}.txt"
    print(f"DEBUG gareko path: {path}, exists: {path.exists()}")
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
        print(f"DEBUG gareko text length: {len(text)}")
        return text


