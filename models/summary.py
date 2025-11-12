from pydantic import BaseModel

class SummaryRequest(BaseModel):
    document_id: str
