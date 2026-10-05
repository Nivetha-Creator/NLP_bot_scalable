from unittest.mock import patch

from nlp_bot_scalable.__init__ import main as run_server


def test_entry_point_starts_uvicorn():
    with patch("uvicorn.run") as mock_run:
        run_server()

        mock_run.assert_called_once_with(
            "nlp_bot_scalable.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
        )
