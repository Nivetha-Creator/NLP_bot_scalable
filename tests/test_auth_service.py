from nlp_bot_scalable.auth.password import verify_password
from nlp_bot_scalable.database.models import User
from nlp_bot_scalable.services.auth_service import AuthService


def test_auth_service_exists():
    service = AuthService()

    assert service is not None


def test_register_hashes_password(db_session):
    service = AuthService()

    result = service.register(
        db_session,
        "alice",
        "alice@example.com",
        "secret123",
    )

    assert result["success"] is True

    user = (
        db_session.query(User)
        .filter(User.email == "alice@example.com")
        .first()
    )

    assert user is not None
    assert user.password != "secret123"
    assert verify_password("secret123", user.password)


def test_login_returns_token(db_session):
    service = AuthService()

    service.register(
        db_session,
        "bob",
        "bob@example.com",
        "secret123",
    )

    result = service.login(
        db_session,
        "bob@example.com",
        "secret123",
    )

    assert result["success"] is True
    assert result["access_token"]
    assert result["token_type"] == "bearer"


def test_login_invalid_password(db_session):
    service = AuthService()

    service.register(
        db_session,
        "carol",
        "carol@example.com",
        "secret123",
    )

    result = service.login(
        db_session,
        "carol@example.com",
        "wrong-password",
    )

    assert result["success"] is False
    assert result["message"] == "Invalid email or password."


def test_register_duplicate_user(db_session):
    service = AuthService()

    service.register(
        db_session,
        "dana",
        "dana@example.com",
        "secret123",
    )

    result = service.register(
        db_session,
        "dana",
        "dana@example.com",
        "other-password",
    )

    assert result["success"] is False
    assert result["message"] == "Username or email already exists."
