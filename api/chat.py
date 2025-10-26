from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.qa_processing import answer_question_gemini

router = APIRouter()

class ChatRequest(BaseModel):
    document_id: str
    question: str
    api_key: str  

@router.post("/")
async def chat_pdf(request: ChatRequest):
    answer = answer_question_gemini(request.document_id, request.question, request.api_key)
    if not answer:
        raise HTTPException(status_code=404, detail="Document not found or not processed")
    return {"answer": answer}
