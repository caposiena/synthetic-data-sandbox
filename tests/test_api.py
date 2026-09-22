from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_status_endpoint():
    response = client.get("/status")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_generate_endpoint():
    response = client.post(
        "/generate?n_samples=10"
    )

    assert response.status_code == 200
    assert response.json()["samples"] == 10
