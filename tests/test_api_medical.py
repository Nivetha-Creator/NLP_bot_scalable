def test_symptoms_endpoint(client):
    response = client.post(
        "/medical/symptoms",
        json={"symptoms": "fever and cough"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["emergency"] is False
    assert "Common cold or flu" in data["possible_conditions"]


def test_symptoms_emergency_endpoint(client):
    response = client.post(
        "/medical/symptoms",
        json={"symptoms": "chest pain and shortness of breath"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["emergency"] is True


def test_medicine_endpoint(client):
    response = client.post(
        "/medical/medicine",
        json={"medicine": "paracetamol"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["medicine"] == "paracetamol"
    assert "uses" in data


def test_knowledge_endpoint(client):
    response = client.post(
        "/medical/knowledge",
        json={"topic": "fever"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["topic"] == "fever"
    assert "definition" in data


def test_medical_endpoint_requires_json_body(client):
    response = client.post("/medical/symptoms")

    assert response.status_code == 422
