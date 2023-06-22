from unittest.mock import AsyncMock, patch
from fastapi import Request
import pytest
from app.api.trainings_info.service import get_user_training_metrics


@patch("app.api.trainings_info.service.get_calories")
@patch("app.api.trainings_info.service.update_goals_status")
@patch("app.api.trainings_info.service.get_user_goals", new_callable=AsyncMock)
@patch("app.api.trainings_info.service.get_user_trainings", new_callable=AsyncMock)
@pytest.mark.anyio
async def test_get_user_training_metrics_one(
    mock_get_user_trainings,
    mock_get_user_goals,
    mock_update_goals_status,
    mock_get_calories,
):
    mock_get_user_trainings.return_value = [
        {
            "_id": "1",
            "user_id": "123",
            "exercises": [
                {
                    "name": "flexiones",
                    "category": "repeticiones",
                    "amount": "20",
                    "exercise_type": "Fuerza",
                    "finished": True,
                    "time": "01:30:00",
                    "steps": 200,
                },
                {
                    "name": "correr",
                    "category": "Tiempo",
                    "amount": "30",
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "00:30:00",
                    "steps": 4000,
                },
            ],
            "updated": "2023-06-19T04:02:28.601Z",
        }
    ]

    mock_get_user_goals.return_value = {
        "_id": "1",
        "user_id": "123",
        "goals": [
            {
                "title": "Meta de puntos fuerza",
                "training_type": "Fuerza",
                "amount": 20,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            }
        ],
    }

    mock_update_goals_status.return_value = {
        "_id": "1",
        "user_id": "123",
        "goals": [
            {
                "title": "Meta de puntos fuerza",
                "training_type": "Fuerza",
                "amount": 20,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 100,
                "completed": True,
            }
        ],
    }

    mock_get_calories.side_effect = [600, 280]

    user_id = "123"
    mock_request = AsyncMock(spec=Request)
    result = await get_user_training_metrics(user_id=user_id, request=mock_request)

    mock_get_user_trainings.assert_called()
    mock_get_user_goals.assert_called()
    mock_update_goals_status.assert_called()
    assert mock_get_calories.call_count == 2

    assert result.distance == 3150
    assert result.time.hour == 2
    assert result.calories == 880
    assert result.milestones == 1


@patch("app.api.trainings_info.service.get_calories")
@patch("app.api.trainings_info.service.update_goals_status")
@patch("app.api.trainings_info.service.get_user_goals", new_callable=AsyncMock)
@patch("app.api.trainings_info.service.get_user_trainings", new_callable=AsyncMock)
@pytest.mark.anyio
async def test_get_user_training_metrics_two(
    mock_get_user_trainings,
    mock_get_user_goals,
    mock_update_goals_status,
    mock_get_calories,
):
    mock_get_user_trainings.return_value = [
        {
            "_id": "1",
            "user_id": "123",
            "exercises": [
                {
                    "name": "flexiones",
                    "category": "repeticiones",
                    "amount": "20",
                    "exercise_type": "Fuerza",
                    "finished": True,
                    "time": "00:30:00",
                    "steps": 200,
                },
                {
                    "name": "correr",
                    "category": "Tiempo",
                    "amount": "30",
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "00:30:00",
                    "steps": 4000,
                },
            ],
            "updated": "2023-06-19T04:02:28.601Z",
        },
        {
            "_id": "2",
            "user_id": "123",
            "exercises": [
                {
                    "name": "flexiones",
                    "category": "repeticiones",
                    "amount": "40",
                    "exercise_type": "Fuerza",
                    "finished": True,
                    "time": "00:30:00",
                    "steps": 200,
                },
                {
                    "name": "correr",
                    "category": "Tiempo",
                    "amount": "90",
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "01:30:00",
                    "steps": 12000,
                },
            ],
            "updated": "2023-06-19T04:02:28.601Z",
        },
    ]

    mock_get_user_goals.return_value = {
        "_id": "1",
        "user_id": "123",
        "goals": [
            {
                "title": "Meta de puntos fuerza",
                "training_type": "Fuerza",
                "amount": 200,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            }
        ],
    }

    mock_update_goals_status.return_value = {
        "_id": "1",
        "user_id": "123",
        "goals": [
            {
                "title": "Meta de puntos fuerza",
                "training_type": "Fuerza",
                "amount": 20,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 30,
                "completed": False,
            }
        ],
    }

    mock_get_calories.side_effect = [200, 280, 200, 840]

    user_id = "123"
    mock_request = AsyncMock(spec=Request)
    result = await get_user_training_metrics(user_id=user_id, request=mock_request)

    mock_get_user_trainings.assert_called()
    mock_get_user_goals.assert_called()
    mock_update_goals_status.assert_called()
    assert mock_get_calories.call_count == 4

    assert result.distance == 12300
    assert result.time.hour == 3
    assert result.calories == 1520
    assert result.milestones == 0


@patch("app.api.trainings_info.service.get_calories")
@patch("app.api.trainings_info.service.update_goals_status")
@patch("app.api.trainings_info.service.get_user_goals", new_callable=AsyncMock)
@patch("app.api.trainings_info.service.get_user_trainings", new_callable=AsyncMock)
@pytest.mark.anyio
async def test_get_user_training_metrics_three(
    mock_get_user_trainings,
    mock_get_user_goals,
    mock_update_goals_status,
    mock_get_calories,
):
    mock_get_user_trainings.return_value = [
        {
            "_id": "1",
            "user_id": "123",
            "exercises": [
                {
                    "name": "flexiones",
                    "category": "repeticiones",
                    "amount": "20",
                    "exercise_type": "Fuerza",
                    "finished": True,
                    "time": "00:30:00",
                    "steps": 200,
                },
                {
                    "name": "correr",
                    "category": "Tiempo",
                    "amount": "30",
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "00:30:00",
                    "steps": 4000,
                },
            ],
            "updated": "2023-06-19T04:02:28.601Z",
        },
        {
            "_id": "2",
            "user_id": "123",
            "exercises": [
                {
                    "name": "flexiones",
                    "category": "repeticiones",
                    "amount": "40",
                    "exercise_type": "Fuerza",
                    "finished": True,
                    "time": "00:30:00",
                    "steps": 200,
                },
                {
                    "name": "correr",
                    "category": "Tiempo",
                    "amount": "90",
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "01:30:00",
                    "steps": 12000,
                },
            ],
            "updated": "2023-06-19T04:02:28.601Z",
        },
    ]

    mock_get_user_goals.return_value = {
        "_id": "1",
        "user_id": "123",
        "goals": [
            {
                "title": "Meta de steps cardio",
                "training_type": "Cardio",
                "amount": 20000,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            }
        ],
    }

    mock_update_goals_status.return_value = {
        "_id": "1",
        "user_id": "123",
        "goals": [
            {
                "title": "Meta de puntos fuerza",
                "training_type": "Fuerza",
                "amount": 20000,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 80,
                "completed": False,
            }
        ],
    }

    mock_get_calories.side_effect = [200, 280, 200, 840]

    user_id = "123"
    mock_request = AsyncMock(spec=Request)
    result = await get_user_training_metrics(user_id=user_id, request=mock_request)

    mock_get_user_trainings.assert_called()
    mock_get_user_goals.assert_called()
    mock_update_goals_status.assert_called()
    assert mock_get_calories.call_count == 4

    assert result.distance == 12300
    assert result.time.hour == 3
    assert result.calories == 1520
    assert result.milestones == 0


@patch("app.api.trainings_info.service.get_calories")
@patch("app.api.trainings_info.service.update_goals_status")
@patch("app.api.trainings_info.service.get_user_goals", new_callable=AsyncMock)
@patch("app.api.trainings_info.service.get_user_trainings", new_callable=AsyncMock)
@pytest.mark.anyio
async def test_get_user_training_metrics_no_trainings(
    mock_get_user_trainings,
    mock_get_user_goals,
    mock_update_goals_status,
    mock_get_calories,
):
    mock_get_user_trainings.return_value = None

    mock_get_user_goals.return_value = {
        "_id": "1",
        "user_id": "123",
        "goals": [
            {
                "title": "Meta de puntos fuerza",
                "training_type": "Fuerza",
                "amount": 200,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            }
        ],
    }

    mock_update_goals_status.return_value = {
        "_id": "1",
        "user_id": "123",
        "goals": [
            {
                "title": "Meta de puntos fuerza",
                "training_type": "Fuerza",
                "amount": 200,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            }
        ],
    }

    mock_get_calories.side_effect = 0

    user_id = "123"
    mock_request = AsyncMock(spec=Request)
    result = await get_user_training_metrics(user_id=user_id, request=mock_request)

    mock_get_user_trainings.assert_called_once()
    assert mock_get_calories.call_count == 0

    assert result.distance == 0.0
    assert result.time.hour == 0
    assert result.calories == 0
    assert result.milestones == 0
