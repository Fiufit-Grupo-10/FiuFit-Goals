from app.main import app
from httpx import AsyncClient
import pytest


def test_load_training(test_app):
    exercises = [
        {
            "name": "flexiones",
            "category": "repeticiones",
            "amount": "20",
            "exercise_type": "Fuerza",
            "finished": True,
            "time": "01:10:15",
        }
    ]

    response = test_app.post(
        "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training", json=exercises
    )
    assert response.status_code == 201

    body = response.json()
    assert "_id" in body


@pytest.mark.anyio
async def test_get_trainings(test_app):
    exercises = [
        {
            "name": "flexiones",
            "category": "repeticiones",
            "amount": "20",
            "exercise_type": "Fuerza",
            "finished": True,
            "time": "01:10:15",
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training", json=exercises
        )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training")

    assert response.status_code == 200
    assert response.json()[0]["user_id"] == "c59710ef-f5d0-41ba-a787-ad8eb739ef4c"
