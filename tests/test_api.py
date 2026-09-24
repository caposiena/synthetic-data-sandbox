from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_status_endpoint():
    response = client.get("/status")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


def test_generate_requires_positive_samples():
    response = client.post(
        "/generate?n_samples=0"
    )

    assert response.status_code == 400


def test_statistics_endpoint():
    response = client.get("/statistics")

    assert response.status_code in {200, 400}
