from unittest.mock import patch

import pytest

from nlp_bot_scalable.nlp.nltk_setup import ensure_nltk_data


@pytest.fixture(autouse=True)
def reset_nltk_ready_flag():
    import nlp_bot_scalable.nlp.nltk_setup as nltk_setup_module

    nltk_setup_module._NLTK_READY = False
    yield
    nltk_setup_module._NLTK_READY = False


def test_ensure_nltk_data_downloads_once():
    with patch("nltk.download") as mock_download:
        ensure_nltk_data()
        assert mock_download.call_count == 3

        mock_download.reset_mock()
        ensure_nltk_data()
        mock_download.assert_not_called()
