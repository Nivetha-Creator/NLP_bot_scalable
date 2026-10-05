def _register_and_login(client, username, email, password):
    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    token = login_response.json()["access_token"]
    return {
        "Authorization": f"Bearer {token}",
    }


def test_chat_with_valid_token(client):
    headers = _register_and_login(
        client,
        "chat_user",
        "chat_user@example.com",
        "secret123",
    )

    response = client.post(
        "/chat",
        json={"message": "hello"},
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["response"]
    assert data["intent"]


def test_chat_history_with_valid_token(client):
    headers = _register_and_login(
        client,
        "history_user",
        "history_user@example.com",
        "secret123",
    )

    chat_response = client.post(
        "/chat",
        json={"message": "hello"},
        headers=headers,
    )
    assert chat_response.status_code == 200

    history_response = client.get(
        "/chat/history",
        headers=headers,
    )

    assert history_response.status_code == 200
    history = history_response.json()
    assert len(history) == 1
    assert history[0]["user_message"] == "hello"
