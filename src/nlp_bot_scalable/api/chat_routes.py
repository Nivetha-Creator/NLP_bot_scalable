from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.config.database import SessionLocal
from src.nlp_bot_scalable.database.chat_repository import get_chat_history
from src.nlp_bot_scalable.services.chat_service import ChatService


router = APIRouter(
    tags=["Chat"]
)

chat_service = ChatService()


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Message to send to the chatbot"
    )
    user_id: int


class ChatResponse(BaseModel):
    intent: str | None
    probability: str | None
    response: str


class ChatHistoryResponse(BaseModel):
    id: int
    user_message: str
    bot_response: str
    intent: str | None


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    return chat_service.chat(
        db,
        request.message,
        request.user_id
    )


@router.get(
    "/chat/history",
    response_model=list[ChatHistoryResponse]
)
def chat_history(
    user_id: int,
    db: Session = Depends(get_db)
):
    return get_chat_history(
        db,
        user_id
    )