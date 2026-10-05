import nltk

_NLTK_READY = False


def ensure_nltk_data() -> None:
    global _NLTK_READY

    if _NLTK_READY:
        return

    for package in ("punkt", "punkt_tab", "wordnet"):
        nltk.download(package, quiet=True)

    _NLTK_READY = True
