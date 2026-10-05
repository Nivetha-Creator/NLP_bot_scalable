def test_cors_allows_configured_origin(client):
    response = client.get(
        "/health",
        headers={"Origin": "http://localhost:8000"},
    )

    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin")
        == "http://localhost:8000"
    )


def test_cors_does_not_reflect_unknown_origin(client):
    response = client.get(
        "/health",
        headers={"Origin": "http://evil.example"},
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") is None
