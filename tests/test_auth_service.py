from nlp_bot_scalable.services.auth_service import AuthService


def test_auth_service_exists():
    service = AuthService()

    assert service is not None