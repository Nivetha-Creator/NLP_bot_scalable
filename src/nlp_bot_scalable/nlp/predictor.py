import json
import random
from pathlib import Path

import numpy as np

from nlp_bot_scalable.nlp.model_loader import load_chatbot
from nlp_bot_scalable.nlp.preprocessing import bag_of_words

PROJECT_ROOT = Path(__file__).resolve().parents[3]
INTENTS_FILE = PROJECT_ROOT / "intents.json"


class ChatbotPredictor:

    def __init__(self):
        self._model = None
        self._words = None
        self._classes = None
        self._intents = None

    def _ensure_loaded(self) -> None:
        if self._model is not None:
            return

        self._model, self._words, self._classes = load_chatbot()

        with open(INTENTS_FILE, "r", encoding="utf-8") as file:
            self._intents = json.load(file)["intents"]

    def predict(self, sentence: str):
        self._ensure_loaded()

        bow = bag_of_words(sentence, self._words)

        results = self._model.predict(
            np.array([bow]),
            verbose=0,
        )[0]

        error_threshold = 0.25

        filtered_results = [
            [index, probability]
            for index, probability in enumerate(results)
            if probability > error_threshold
        ]

        filtered_results.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        if not filtered_results:
            return {
                "intent": None,
                "probability": None,
                "response": "Sorry, I didn't understand that.",
            }

        best_intent = self._classes[filtered_results[0][0]]
        best_probability = filtered_results[0][1]
        response = "Sorry, I didn't understand that."

        for intent in self._intents:
            if intent["tag"] == best_intent:
                response = random.choice(intent["responses"])
                break

        return {
            "intent": best_intent,
            "probability": str(best_probability),
            "response": response,
        }


if __name__ == "__main__":
    predictor = ChatbotPredictor()
    result = predictor.predict("Hello")
    print(result)
