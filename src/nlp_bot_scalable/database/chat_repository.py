from sqlalchemy.orm import Session

from src.nlp_bot_scalable.database.models import ChatMessage


def save_chat(
    db: Session,
    user_id: int,
    user_message: str,
    bot_response: str,
    intent: str | None = None,
):
    chat = ChatMessage(
        user_id=user_id,
        user_message=user_message,
        bot_response=bot_response,
        intent=intent,
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat


def get_chat_history(
    db: Session,
    user_id: int
):
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.user_id == user_id)
        .order_by(ChatMessage.id.asc())
        .all()
    )