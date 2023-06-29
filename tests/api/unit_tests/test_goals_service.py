from unittest.mock import patch
import pytest
from app.api.goals.service import get_calories, update_goals_status


@pytest.mark.anyio
async def test_goals_get_calories():
    response = get_calories(
        exercise_type="Fuerza",
        total_time="01:30:00",
        weigth=80,
        category_multipliers={"Fuerza": 5},
    )
    assert response == 600


@patch("app.api.goals.service.get_calories")
@pytest.mark.anyio
async def test_goals_update_goals_status_calories(mock_get_calories):
    mock_get_calories.return_value = 700

    goals = {
        "_id": "1",
        "user_id": "10",
        "goals": [
            {
                "title": "Meta de fuerza",
                "training_type": "Fuerza",
                "amount": 30,
                "goal_type": "calories",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            }
        ],
    }

    trainings = [
        {
            "_id": "1",
            "user_id": "10",
            "exercises": [
                {
                    "name": "flexiones",
                    "category": "repeticiones",
                    "amount": 40,
                    "exercise_type": "Fuerza",
                    "finished": True,
                    "time": "01:45:00",
                }
            ],
            "updated": "2023-06-19T04:04:21.410Z",
        }
    ]

    response = update_goals_status(goals=goals, trainings=trainings, weigth=80)
    mock_get_calories.assert_called()
    assert response == {
        "_id": "1",
        "user_id": "10",
        "goals": [
            {
                "title": "Meta de fuerza",
                "training_type": "Fuerza",
                "amount": 30,
                "goal_type": "calories",
                "limit": "-",
                "notified": False,
                "percentage": 100,
                "completed": True,
            }
        ],
    }


@patch("app.api.goals.service.get_calories")
@pytest.mark.anyio
async def test_goals_update_goals_status_points(mock_get_calories):
    mock_get_calories.return_value = 700

    goals = {
        "_id": "1",
        "user_id": "10",
        "goals": [
            {
                "title": "Meta de fuerza",
                "training_type": "Fuerza",
                "amount": 30,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            },
            {
                "title": "Meta de Cardio",
                "training_type": "Cardio",
                "amount": 100,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            },
        ],
    }

    trainings = [
        {
            "_id": "1",
            "user_id": "10",
            "exercises": [
                {
                    "name": "flexiones",
                    "category": "repeticiones",
                    "amount": 40,
                    "exercise_type": "Fuerza",
                    "finished": True,
                    "time": "01:45:00",
                },
                {
                    "name": "correr",
                    "category": "tiempo",
                    "amount": 30,
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "00:30:00",
                },
            ],
            "updated": "2023-06-19T04:04:21.410Z",
        },
        {
            "_id": "2",
            "user_id": "10",
            "exercises": [
                {
                    "name": "correr",
                    "category": "tiempo",
                    "amount": 40,
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "00:40:10",
                }
            ],
            "updated": "2023-06-19T04:04:21.410Z",
        },
    ]

    response = update_goals_status(goals=goals, trainings=trainings, weigth=80)
    mock_get_calories.assert_not_called()
    assert response == {
        "_id": "1",
        "user_id": "10",
        "goals": [
            {
                "title": "Meta de fuerza",
                "training_type": "Fuerza",
                "amount": 30,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 100,
                "completed": True,
            },
            {
                "title": "Meta de Cardio",
                "training_type": "Cardio",
                "amount": 100,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 70,
                "completed": False,
            },
        ],
    }


@patch("app.api.goals.service.get_calories")
@pytest.mark.anyio
async def test_goals_update_goals_status_steps(mock_get_calories):
    mock_get_calories.return_value = 700

    goals = {
        "_id": "1",
        "user_id": "10",
        "goals": [
            {
                "title": "Meta de steps",
                "training_type": "Cardio",
                "amount": 1000,
                "goal_type": "steps",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            },
        ],
    }

    trainings = [
        {
            "_id": "1",
            "user_id": "10",
            "exercises": [
                {
                    "name": "caminar",
                    "category": "repeticiones",
                    "amount": 5,
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "00:05:00",
                    "steps": 300,
                },
                {
                    "name": "correr",
                    "category": "tiempo",
                    "amount": 10,
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "00:10:00",
                    "steps": 800,
                },
            ],
            "updated": "2023-06-19T04:04:21.410Z",
        },
    ]

    response = update_goals_status(goals=goals, trainings=trainings, weigth=80)
    mock_get_calories.assert_not_called()
    assert response == {
        "_id": "1",
        "user_id": "10",
        "goals": [
            {
                "title": "Meta de steps",
                "training_type": "Cardio",
                "amount": 1000,
                "goal_type": "steps",
                "limit": "-",
                "notified": False,
                "percentage": 100,
                "completed": True,
            },
        ],
    }


@patch("app.api.goals.service.get_calories")
@pytest.mark.anyio
async def test_goals_update_goals_status_all(mock_get_calories):
    mock_get_calories.side_effect = [280, 560]

    goals = {
        "_id": "1",
        "user_id": "10",
        "goals": [
            {
                "title": "Meta de fuerza",
                "training_type": "Fuerza",
                "amount": 30,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            },
            {
                "title": "Meta de Cardio",
                "training_type": "Cardio",
                "amount": 1000,
                "goal_type": "calories",
                "limit": "-",
                "notified": False,
                "percentage": 0,
                "completed": False,
            },
        ],
    }

    trainings = [
        {
            "_id": "1",
            "user_id": "10",
            "exercises": [
                {
                    "name": "flexiones",
                    "category": "repeticiones",
                    "amount": 40,
                    "exercise_type": "Fuerza",
                    "finished": True,
                    "time": "01:45:00",
                },
                {
                    "name": "correr",
                    "category": "tiempo",
                    "amount": 30,
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "00:30:00",
                },
            ],
            "updated": "2023-06-19T04:04:21.410Z",
        },
        {
            "_id": "2",
            "user_id": "10",
            "exercises": [
                {
                    "name": "correr",
                    "category": "tiempo",
                    "amount": 40,
                    "exercise_type": "Cardio",
                    "finished": True,
                    "time": "01:00:00",
                }
            ],
            "updated": "2023-06-19T04:04:21.410Z",
        },
    ]

    response = update_goals_status(goals=goals, trainings=trainings, weigth=80)
    assert mock_get_calories.call_count == 2
    assert response == {
        "_id": "1",
        "user_id": "10",
        "goals": [
            {
                "title": "Meta de fuerza",
                "training_type": "Fuerza",
                "amount": 30,
                "goal_type": "points",
                "limit": "-",
                "notified": False,
                "percentage": 100,
                "completed": True,
            },
            {
                "title": "Meta de Cardio",
                "training_type": "Cardio",
                "amount": 1000,
                "goal_type": "calories",
                "limit": "-",
                "notified": False,
                "percentage": 84.0,
                "completed": False,
            },
        ],
    }
