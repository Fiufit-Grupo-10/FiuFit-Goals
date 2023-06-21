from app.config.database import TRAININGS_COLLECTION_NAME
from app.main import app
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
import pytest


@pytest.mark.anyio
async def test_load_training(test_app, cleanup):
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
    assert response.status_code == 201

    body = response.json()
    assert "_id" in body


@pytest.mark.anyio
async def test_get_trainings(cleanup):
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


@pytest.mark.anyio
async def test_get_trainings_metrics_all(cleanup):
    exercises1 = [
        {
            "name": "flexiones",
            "category": "repeticiones",
            "amount": "20",
            "exercise_type": "Fuerza",
            "finished": True,
            "time": "01:10:00",
        },
        {
            "name": "Correr",
            "category": "tiempo",
            "amount": "20",
            "exercise_type": "Cardio",
            "finished": True,
            "time": "00:20:00",
        },
    ]

    exercises2 = [
        {
            "name": "Correr",
            "category": "tiempo",
            "amount": "30",
            "exercise_type": "Cardio",
            "finished": True,
            "time": "00:30:00",
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response1 = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training", json=exercises1
        )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response2 = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training", json=exercises2
        )

    assert response1.status_code == 201
    assert response2.status_code == 201

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training/metrics"
        )

    assert response.status_code == 200
    assert response.json()["distance"] == 0
    assert response.json()["time"] == "02:00:00"
    assert response.json()["calories"] == 933.3333333333334
    assert response.json()["milestones"] == 0


@pytest.mark.anyio
async def test_get_trainings_metrics_timestamp_filter(cleanup):
    exercises1 = [
        {
            "name": "flexiones",
            "category": "repeticiones",
            "amount": "20",
            "exercise_type": "Fuerza",
            "finished": True,
            "time": "01:10:00",
        },
        {
            "name": "Correr",
            "category": "tiempo",
            "amount": "20",
            "exercise_type": "Cardio",
            "finished": True,
            "time": "00:20:00",
        },
    ]

    exercises2 = [
        {
            "name": "Correr",
            "category": "tiempo",
            "amount": "30",
            "exercise_type": "Cardio",
            "finished": True,
            "time": "00:30:00",
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response1 = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training", json=exercises1
        )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response2 = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training", json=exercises2
        )

    assert response1.status_code == 201
    assert response2.status_code == 201
    id = response2.json()["_id"]

    # Editing timestamp to check this training is filtered
    async with AsyncClient(app=app, base_url="http://test") as ac:
        training = await app.mongodb[TRAININGS_COLLECTION_NAME].find_one({"_id": id})
        # Changing date to may
        training["updated"] = "2023-05-18T23:23:23.656470"
        training = jsonable_encoder(training)
        await app.mongodb[TRAININGS_COLLECTION_NAME].delete_one({"_id": id})
        await app.mongodb[TRAININGS_COLLECTION_NAME].insert_one(training)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        query = "?start_date=2023-06-01T23%3A23%3A23.656470&end_date=2023-12-31T10%3A23%3A23.656470"
        response = await ac.get(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training/metrics" + query
        )

    assert response.status_code == 200
    assert response.json()["distance"] == 0
    assert response.json()["time"] == "01:30:00"
    assert response.json()["calories"] == 653.3333333333334
    assert response.json()["milestones"] == 0


@pytest.mark.anyio
async def test_get_trainings_metrics_none(cleanup):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training/metrics"
        )

    assert response.status_code == 200
    assert response.json()["distance"] == 0
    assert response.json()["time"] == "00:00:00"
    assert response.json()["calories"] == 0
    assert response.json()["milestones"] == 0


@pytest.mark.anyio
async def test_get_trainings_metrics_all_with_milestone(cleanup):
    exercises1 = [
        {
            "name": "flexiones",
            "category": "repeticiones",
            "amount": "20",
            "exercise_type": "Fuerza",
            "finished": True,
            "time": "01:10:00",
        },
        {
            "name": "Correr",
            "category": "tiempo",
            "amount": "20",
            "exercise_type": "Cardio",
            "finished": True,
            "time": "00:20:00",
        },
    ]

    exercises2 = [
        {
            "name": "Correr",
            "category": "tiempo",
            "amount": "30",
            "exercise_type": "Cardio",
            "finished": True,
            "time": "00:30:00",
        }
    ]

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response1 = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training", json=exercises1
        )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response2 = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training", json=exercises2
        )

    assert response1.status_code == 201
    assert response2.status_code == 201

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
        response3 = await ac.post(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/goals", json=goals
        )
    assert response3.status_code == 201

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(
            "/users/c59710ef-f5d0-41ba-a787-ad8eb739ef4c/training/metrics"
        )

    assert response.status_code == 200
    assert response.json()["distance"] == 0
    assert response.json()["time"] == "02:00:00"
    assert response.json()["calories"] == 933.3333333333334
    assert response.json()["milestones"] == 1
