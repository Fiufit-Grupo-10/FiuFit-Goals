from app.main import app
from httpx import AsyncClient
import pytest


@pytest.mark.anyio
async def test_create_goals(test_app, cleanup):
    goals = [
        {
            "title": "meta1",
            "training_type": "Cardio",
            "amount": 100,
            "goal_type": "calories",
            "limit": "27-08-23",
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=goals
        )
    assert response.status_code == 201

    body = response.json()
    assert "_id" in body


@pytest.mark.anyio
async def test_create_goals_error(test_app, cleanup):
    goals = [
        {
            "title": "meta1",
            "training_type": "Cardio",
            "amount": 100,
            "goal_type": "calories",
            "limit": "27-08-23",
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=goals
        )
    assert response.status_code == 201

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=goals
        )
    assert response.status_code == 409


@pytest.mark.anyio
async def test_create_goals_with_incorrect_type(test_app, cleanup):
    goals = [
        {
            "title": "meta1",
            "training_type": "Cardio",
            "amount": 100,
            "goal_type": "running",
            "limit": "27-08-23",
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=goals
        )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_update_goals(test_app, cleanup):
    goals = [
        {
            "title": "meta1",
            "training_type": "Cardio",
            "amount": 100,
            "goal_type": "calories",
            "limit": "27-08-23",
        },
        {
            "title": "meta2",
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

    updated_goals = [
        {
            "title": "meta1",
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

    expected = updated_goals
    expected[0]["completed"] = False
    expected[0]["notified"] = False
    expected[0]["percentage"] = 0.0
    assert response.status_code == 200
    assert response.json()["goals"] == expected


@pytest.mark.anyio
async def test_get_goals(test_app, cleanup):
    goals = [
        {
            "title": "meta1",
            "training_type": "Cardio",
            "amount": 100,
            "goal_type": "calories",
            "limit": "27-08-23",
        },
        {
            "title": "meta2",
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

    expected = goals
    expected[0]["completed"] = False
    expected[0]["notified"] = False
    expected[0]["percentage"] = 0.0
    expected[1]["completed"] = False
    expected[1]["notified"] = False
    expected[1]["percentage"] = 0.0

    assert response.status_code == 200
    assert response.json()["goals"] == expected
