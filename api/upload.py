# api/upload.py
from fastapi import APIRouter, UploadFile, File
import random
from pathlib import Path
from PyPDF2 import PdfReader


router = APIRouter()

PDF_TEXT_DIR = Path("pdf_texts")
PDF_TEXT_DIR.mkdir(exist_ok=True)

pdf_text_store = {}

async def save_pdf_text(file: UploadFile, document_id: str):
    """Extract text from uploaded PDF and save as a .txt file."""
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    # Save text to file
    text_file_path = PDF_TEXT_DIR / f"{document_id}.txt"
    with open(text_file_path, "w", encoding="utf-8") as f:
        f.write(text)

    return text

@router.post("/")
async def upload_pdf(file: UploadFile):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Generate unique document_id
    document_id = str("document" + str(random.randint(0, 100)))

    # Save PDF text
    text = await save_pdf_text(file, document_id)

    return {"document_id": document_id, "message": f"PDF processed, {len(text)} characters extracted"}