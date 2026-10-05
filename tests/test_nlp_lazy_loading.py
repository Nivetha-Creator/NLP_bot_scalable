import json
from unittest.mock import MagicMock, mock_open, patch

from nlp_bot_scalable.nlp.predictor import ChatbotPredictor
from nlp_bot_scalable.services.chat_service import ChatService


def test_chat_service_does_not_create_predictor_on_init():
    with patch("nlp_bot_scalable.services.chat_service.ChatbotPredictor") as mock_predictor:
        ChatService()
        mock_predictor.assert_not_called()


def test_predictor_lazy_loads_model():
    intents_payload = {
        "intents": [
            {
                "tag": "greeting",
                "responses": ["Hello there!"],
            }
        ]
    }
    mock_model = MagicMock()
    mock_model.predict.return_value = [[0.9]]

    with patch("nlp_bot_scalable.nlp.predictor.load_chatbot") as mock_load:
        mock_load.return_value = (mock_model, ["hello"], ["greeting"])

        with patch(
            "builtins.open",
            mock_open(read_data=json.dumps(intents_payload)),
        ):
            predictor = ChatbotPredictor()
            mock_load.assert_not_called()

            result = predictor.predict("hello")

            mock_load.assert_called_once()
            assert result["intent"] == "greeting"
            assert result["response"] == "Hello there!"
