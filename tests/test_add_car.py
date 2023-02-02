from unittest.mock import Mock
from fastapi.testclient import TestClient

from carsharing import app
from routers.cars import add_car
from schemas import CarInput, User, Car

client = TestClient(app)


def test_add_car():
    response = client.post(
        "/api/cars/",
        json={
            "doors": 7,
            "size": "l",

        },
        headers={
            "Authorization": "Bearer nick"
        }
    )

    assert response.status_code == 200
    car = response.json()

    assert car["doors"] == 7
    assert car["size"] == "l"


def test_add_car_session():
    mock_session = Mock()
    input = CarInput(doors=6, size="l")
    user = User(username="nick")
    result = add_car(car=input, session=mock_session, user=user)

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    assert isinstance(result, Car)
    assert result.doors == 6
    assert result.size == "l"

