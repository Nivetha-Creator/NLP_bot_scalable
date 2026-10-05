import numpy as np
import nltk

from nltk.stem import WordNetLemmatizer

from nlp_bot_scalable.nlp.nltk_setup import ensure_nltk_data

lemmatizer = WordNetLemmatizer()


def clean_up_sentence(sentence: str) -> list[str]:
    ensure_nltk_data()
    sentence_words = nltk.word_tokenize(sentence)

    return [
        lemmatizer.lemmatize(word.lower())
        for word in sentence_words
    ]


def bag_of_words(sentence: str, words: list[str]) -> np.ndarray:
    sentence_words = clean_up_sentence(sentence)

    bag = [0] * len(words)

    for word in sentence_words:
        for index, vocabulary_word in enumerate(words):
            if vocabulary_word == word:
                bag[index] = 1

    return np.array(bag)
