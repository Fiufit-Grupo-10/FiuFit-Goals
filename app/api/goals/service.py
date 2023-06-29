import datetime
from fastapi import Request
import httpx
from app.api.goals import crud as goals_crud
from app.api.trainings_info import crud as trainings_crud
from app.api.goals.models import Goal
from app.config.config import USERS_SERVICE_URL, DEFAULT_WEIGTH, CATEGORY_MULTIPLIERS


async def create_user_goals(user_id: str, goals: list[Goal], request: Request):
    old_goals = await goals_crud.get_user_goals(user_id=user_id, request=request)
    if old_goals is not None:
        raise Exception

    goals = await goals_crud.create_user_goals(
        user_id=user_id, goals=goals, request=request
    )

    trainings = await trainings_crud.get_user_trainings(
        user_id=user_id, request=request
    )

    if trainings is None:
        return goals

    weigth = get_user_weigth(user_id=user_id)

    return update_goals_status(goals=goals, trainings=trainings, weigth=weigth)


async def update_user_goals(user_id: str, goals: list[Goal], request: Request):
    new_goals = await goals_crud.update_user_goals(
        user_id=user_id, goals=goals, request=request
    )

    trainings = await trainings_crud.get_user_trainings(
        user_id=user_id, request=request
    )

    if trainings is None:
        return new_goals

    weigth = get_user_weigth(user_id=user_id)

    return update_goals_status(goals=new_goals, trainings=trainings, weigth=weigth)


async def get_user_goals(user_id: str, request: Request):
    new_goals = await goals_crud.get_user_goals(user_id=user_id, request=request)
    if new_goals is None:
        return None

    trainings = await trainings_crud.get_user_trainings(
        user_id=user_id, request=request
    )

    if trainings is None:
        return new_goals

    weigth = get_user_weigth(user_id=user_id)

    return update_goals_status(goals=new_goals, trainings=trainings, weigth=weigth)


def update_goals_status(goals, trainings, weigth):
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
                            weigth=weigth,
                        )
                    if goal_type == "steps":
                        score += exercise["steps"]

        percentage = 0
        if score > 0:
            percentage = score / goal["amount"] * 100
        if percentage > 100:
            goal["completed"] = True
            goal["percentage"] = 100
        else:
            goal["percentage"] = percentage
            goal["completed"] = False

    return goals


# METS
def get_calories(
    exercise_type,
    total_time,
    weigth,
    category_multipliers=CATEGORY_MULTIPLIERS,
):
    hours, minutes, seconds = map(int, total_time.split(":"))
    time_obj = datetime.time(hours, minutes, seconds)
    hours = time_obj.hour + time_obj.minute / 60 + time_obj.second / 3600

    return weigth * category_multipliers[exercise_type] * hours


def get_user_weigth(user_id: str) -> int:
    if USERS_SERVICE_URL != "":
        url = USERS_SERVICE_URL + "users/" + user_id
        response = httpx.get(url)
        return response.json()["weigth"]
    else:
        return DEFAULT_WEIGTH
