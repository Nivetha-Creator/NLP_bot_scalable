def _register_user(client, username, email, password):
    return client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )


def _login_user(client, email, password):
    return client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )


def test_register_and_login_returns_token(client):
    register_response = _register_user(
        client,
        "api_user",
        "api_user@example.com",
        "secret123",
    )

    assert register_response.status_code == 200
    register_data = register_response.json()
    assert register_data["success"] is True
    assert register_data.get("access_token") is None

    login_response = _login_user(
        client,
        "api_user@example.com",
        "secret123",
    )

    assert login_response.status_code == 200
    login_data = login_response.json()
    assert login_data["success"] is True
    assert login_data["access_token"]
    assert login_data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    _register_user(
        client,
        "invalid_login_user",
        "invalid_login@example.com",
        "secret123",
    )

    login_response = _login_user(
        client,
        "invalid_login@example.com",
        "wrong-password",
    )

    assert login_response.status_code == 200
    assert login_response.json()["success"] is False


def test_chat_requires_authentication(client):
    response = client.post(
        "/chat",
        json={"message": "hello"},
    )

    assert response.status_code in (401, 403)


def test_chat_history_requires_authentication(client):
    response = client.get("/chat/history")

    assert response.status_code in (401, 403)
