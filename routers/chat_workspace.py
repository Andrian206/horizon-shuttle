from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
import os
from models.database import get_db
from models.schemas import ChatRequest, ChatResponse
from services.rag import rag_query

router = APIRouter()
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM", "HS256")])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/chat", response_model=ChatResponse)
def chat_workspace(
    request: ChatRequest,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Workspace chat - requires auth.
    Supports 3 modes: assistant, draft, insight.
    """
    result = rag_query(
        query=request.message,
        mode=request.mode,
        user_type="business"
    )
    return ChatResponse(reply=result["reply"], sources=result["sources"])

@router.post("/chat")
def chat_workspace(
    request: ChatRequest,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Create or get session
    if not request.session_id:
        session = ChatSession(
            user_id=get_user_id(username),
            mode=request.mode,
            user_type="business"
        )
        db.add(session)
        db.commit()
        session_id = session.id
    else:
        session_id = request.session_id
    
    # RAG query
    result = rag_query(
        query=request.message,
        mode=request.mode,
        user_type="business"
    )
    
    # Save messages to DB
    # ... (save user message + assistant reply)
    
    return {
        "reply": result["reply"],
        "session_id": session_id,
        "sources": result.get("sources", [])
    }