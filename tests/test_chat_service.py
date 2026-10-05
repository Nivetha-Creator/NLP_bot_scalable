from src.nlp_bot_scalable.services.chat_service import ChatService


def test_chat_service_exists():
    service = ChatService()

    assert service is not None