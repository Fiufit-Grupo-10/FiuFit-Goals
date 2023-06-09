from app.main import app
from httpx import AsyncClient
import pytest


def test_create_goals(test_app):
    goals = [
        {
            "training_type": "Cardio",
            "amount": 100,
            "goal_type": "calories",
            "limit": "27-08-23",
        }
    ]

    response = test_app.post(
        "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=goals
    )
    assert response.status_code == 201

    body = response.json()
    assert "_id" in body


def test_create_goals_with_incorrect_type(test_app):
    goals = [
        {
            "training_type": "Cardio",
            "amount": 100,
            "goal_type": "running",
            "limit": "27-08-23",
        }
    ]

    response = test_app.post(
        "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=goals
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_update_goals(test_app):
    goals = [
        {
            "training_type": "Cardio",
            "amount": 100,
            "goal_type": "calories",
            "limit": "27-08-23",
        },
        {
            "training_type": "Fuerza",
            "amount": 1000,
            "goal_type": "calories",
            "limit": "27-08-23",
        },
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=goals
        )

    # id = response.json()["_id"]

    updated_goals = [
        {
            "training_type": "steps",
            "amount": 5000,
            "goal_type": "steps",
            "limit": "27-08-23",
        },
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=updated_goals
        )

    assert response.status_code == 200
    assert response.json()["goals"] == updated_goals
    # assert response.json()["_id"] == id


@pytest.mark.anyio
async def test_get_goals(test_app):
    goals = [
        {
            "training_type": "Cardio",
            "amount": 100,
            "goal_type": "calories",
            "limit": "27-08-23",
        },
        {
            "training_type": "Fuerza",
            "amount": 1000,
            "goal_type": "calories",
            "limit": "27-08-23",
        },
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=goals
        )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals")

    assert response.status_code == 200
    assert response.json()["goals"] == goals
