from pydantic import BaseModel

class ChatRequest(BaseModel):
    messages: str

class ChatResponse(BaseModel):
    intent: str
    entities: dict
    response: str
