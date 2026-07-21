from fastapi import APIRouter
from models.schemas import ChatRequest, ChatResponse
from services.rag import rag_query

router = APIRouter()

@router.post("", response_model=ChatResponse)
def chat_public(request: ChatRequest):
    """
    Public chat - no auth required.
    Always uses 'assistant' mode and 'public' filter.
    """
    result = rag_query(
        query=request.message,
        mode="assistant",
        user_type="public"
    )
    return ChatResponse(reply=result["reply"], sources=result["sources"])