from nlp_bot_scalable.database.chat_repository import save_chat
from nlp_bot_scalable.database.models import User
from nlp_bot_scalable.services.auth_service import AuthService
from nlp_bot_scalable.services.chat_service import ChatService


def _create_user(db_session, username, email):
    auth = AuthService()
    auth.register(db_session, username, email, "secret123")
    return (
        db_session.query(User)
        .filter(User.email == email)
        .first()
    )


def test_chat_context_scoped_to_user(db_session):
    user_one = _create_user(db_session, "user_one", "user_one@example.com")
    user_two = _create_user(db_session, "user_two", "user_two@example.com")

    save_chat(
        db_session,
        user_id=user_one.id,
        user_message="hi",
        bot_response="Hi! How are you feeling today?",
        intent="greeting",
    )

    service = ChatService()

    user_one_result = service.chat(db_session, "good", user_one.id)
    user_two_result = service.chat(db_session, "good", user_two.id)

    assert user_one_result["intent"] == "conversation_positive"
    assert user_two_result["intent"] != "conversation_positive"
