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
