from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from nlp_bot_scalable.api.dependencies import get_current_user, get_db
from nlp_bot_scalable.database.chat_repository import get_chat_history
from nlp_bot_scalable.database.models import User
from nlp_bot_scalable.services.chat_service import ChatService

router = APIRouter(
    tags=["Chat"],
)

chat_service = ChatService()


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Message to send to the chatbot",
    )


class ChatResponse(BaseModel):
    intent: str | None
    probability: str | None
    response: str


class ChatHistoryResponse(BaseModel):
    id: int
    user_message: str
    bot_response: str
    intent: str | None


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return chat_service.chat(
        db,
        request.message,
        current_user.id,
    )


@router.get(
    "/chat/history",
    response_model=list[ChatHistoryResponse],
)
def chat_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_chat_history(
        db,
        current_user.id,
    )
