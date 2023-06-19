# import datetime
# from fastapi import Request
# from unittest.mock import MagicMock, patch
# import pytest
# import asyncio
# from app.api.trainings_info.service import get_user_training_metrics

# @pytest.mark.anyio
# async def test_get_user_training_metrics():

#     user_id = "123"
#     start_date = "2023-01-01"
#     end_date = "2023-06-01"
#     mock_request = MagicMock(spec=Request)
#     mock_get_user_trainings = MagicMock()
#     mock_get_user_goals = MagicMock()
#     mock_update_user_goals = MagicMock()
#     mock_get_calories = MagicMock()

#     # Setear los valores de retorno esperados para las funciones dependientes
#     mock_get_user_trainings.return_value = [
#         {
#         "_id": "1",
#         "user_id": "123",
#         "exercises": [
#             {
#                 "name": "flexiones",
#                 "category": "repeticiones",
#                 "amount": "20",
#                 "exercise_type": "Fuerza",
#                 "finished": True,
#                 "time": "01:30:00"
#             },
#             {
#                 "name": "correr",
#                 "category": "Tiempo",
#                 "amount": "30",
#                 "exercise_type": "Cardio",
#                 "finished": True,
#                 "time": "00:30:00"
#             }
#         ],
#         "updated": "2023-06-19T04:02:28.601Z"
#         }
#     ]

#     mock_get_user_goals.return_value = {
#         "_id": "1",
#         "user_id": "123",
#         "goals": [
#             {
#             "title": "Meta de puntos fuerza",
#             "training_type": "Fuerza",
#             "amount": 20,
#             "goal_type": "points",
#             "limit": "-",
#             "notified": False,
#             "percentage": 0,
#             "completed": False
#             }
#         ]
#     }

#     mock_update_user_goals.return_value = {
#         "_id": "1",
#         "user_id": "123",
#         "goals": [
#             {
#             "title": "Meta de puntos fuerza",
#             "training_type": "Fuerza",
#             "amount": 20,
#             "goal_type": "points",
#             "limit": "-",
#             "notified": False,
#             "percentage": 100,
#             "completed": True
#             }
#         ]
#     }

#     #mock_goals_service.get_calories.return_values = [600, 280]

#     with patch("app.api.trainings_info.crud.get_user_trainings", mock_get_user_trainings):
#         #patch("get_user_goals", mock_get_user_goals), \
#         #patch("update_user_goals", mock_update_user_goals):
#         # Ejecutar la función bajo prueba
#         result = await get_user_training_metrics(
#             user_id=user_id,
#             request=mock_request,
#             start_date=start_date,
#             end_date=end_date,
#         )


#     # Verificar llamadas a funciones dependientes
#     mock_get_user_trainings.assert_called_once_with(
#         user_id=user_id,
#         request=mock_request,
#         end_date=end_date,
#         start_date=start_date,
#     )

#     # Verificar los resultados
#     assert result.time == datetime.time(2, 0, 0)
#     assert result.distance == 0.0
#     assert result.milestones == 1
#     assert result.calories == 880

#     # mock_goals_crud.get_user_goals.assert_called_once_with(
#     #     user_id=user_id,
#     #     request=mock_request,
#     # )

#     # mock_goals_service.update_goals_status.assert_called_once_with(
#     #     goals=[
#     #         {"goal_id": 1, "completed": True},
#     #         {"goal_id": 2, "completed": False},
#     #     ],
#     #     trainings=[
#     #         {
#     #             "exercises": [
#     #                 {"exercise_type": "running", "time": "00:30:00"},
#     #                 {"exercise_type": "cycling", "time": "01:00:00"},
#     #             ]
#     #         },
#     #         {
#     #             "exercises": [
#     #                 {"exercise_type": "swimming", "time": "00:45:00"},
#     #                 {"exercise_type": "running", "time": "00:45:00"},
#     #             ]
#     #         },
#     #     ],
#     # )

#     # expected_calories_calls = [
#     #     (("running", "00:30:00"), {}),
#     #     (("cycling", "01:00:00"), {}),
#     #     (("swimming", "00:45:00"), {}),
#     #     (("running", "00:45:00"), {}),
#     # ]
#     # mock_goals_service.get_calories.assert_has_calls(
#     #     expected_calories_calls,
#     #     any_order=True
#     # )
