from pydantic import BaseModel
from typing import Optional, List

# Auth
class UserCreate(BaseModel):
    nama: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Chat
class ChatRequest(BaseModel):
    message: str
    mode: Optional[str] = "assistant"  # assistant | draft | insight

class ChatResponse(BaseModel):
    reply: str
    sources: Optional[List[str]] = None

class ChatMessage(BaseModel):
    role: str  # user | assistant
    content: str