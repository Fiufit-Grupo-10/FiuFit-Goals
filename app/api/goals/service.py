import datetime
from fastapi import Request
from app.api.goals import crud as goals_crud
from app.api.trainings_info import crud as trainings_crud
from app.api.goals.models import Goal


async def create_user_goals(user_id: str, goals: list[Goal], request: Request):
    old_goals = await goals_crud.get_user_goals(user_id=user_id,request=request)
    # Todo: Quizas la mejor forma de manejarlo seria tirando una except
    if old_goals is not None:
        return None
    
    goals = await goals_crud.create_user_goals(
        user_id=user_id, goals=goals, request=request
    )

    trainings = await trainings_crud.get_user_trainings(
        user_id=user_id, request=request
    )

    if trainings is None:
        return goals

    return update_goals_status(goals=goals, trainings=trainings)


# todo: Probablemente se pueda refactorizar un poco mas,evitando mas repeticion de codigo
async def update_user_goals(user_id: str, goals: list[Goal], request: Request):
    new_goals = await goals_crud.update_user_goals(
        user_id=user_id, goals=goals, request=request
    )

    trainings = await trainings_crud.get_user_trainings(
        user_id=user_id, request=request
    )

    if trainings is None:
        return new_goals

    return update_goals_status(goals=new_goals, trainings=trainings)


async def get_user_goals(user_id: str, request: Request):
    new_goals = await goals_crud.get_user_goals(user_id=user_id, request=request)

    trainings = await trainings_crud.get_user_trainings(
        user_id=user_id, request=request
    )

    if trainings is None:
        return new_goals

    return update_goals_status(goals=new_goals, trainings=trainings)


def update_goals_status(goals, trainings):
    for goal in goals["goals"]:
        goal_type = goal["goal_type"]
        goal_training_type = goal["training_type"]
        score = 0
        for training in trainings:
            for exercise in training["exercises"]:
                if goal_training_type == exercise["exercise_type"]:
                    if goal_type == "points":
                        score += exercise["amount"]  # Por ahora el mapeo es 1 a 1
                    if goal_type == "calories":
                        score += get_calories(
                            exercise_type=exercise["exercise_type"],
                            total_time=exercise["time"],
                        )

        percentage = 0
        if score > 0:
            percentage = score / goal["amount"] * 100
        if percentage > 100:
            goal["completed"] = True
            goal["percentage"] = 1
        else:
            goal["percentage"] = percentage

    return goals


# Esto es lo de METS
def get_calories(exercise_type, total_time):
    # En principio toma el tiempo que se tardo (No creo que sea el merjo approach)
    hours, minutes, seconds = map(int, total_time.split(":"))
    time_obj = datetime.time(hours, minutes, seconds)
    hours = time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600

    category_multipliers = {
        "Fuerza": 5,
        "Cardio": 7,
        "Yoga": 3,
        "Pilates": 4,
        "Baile": 4,
        "Meditacion": 1,
        "Hiit": 10,
        "Kickboxing": 10,
        "Tonificacion": 4,
        "Spinning": 4,
        "Cinta": 4,
        "Estirar": 2,
    }
    return 80 * category_multipliers[exercise_type] * hours
