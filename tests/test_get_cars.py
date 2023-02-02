from fastapi.testclient import TestClient

from carsharing import app


client = TestClient(app)


def test_get_cars():
    response = client.get("/api/cars/")
    assert response.status_code == 200

    cars = response.json()

    assert all(["doors" in c["Car"] for c in cars])
    assert all(["size" in c["Car"] for c in cars])
