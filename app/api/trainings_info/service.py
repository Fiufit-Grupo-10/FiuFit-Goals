import datetime
from fastapi import Request
from app.api.goals.crud import get_user_goals
from app.api.goals.service import update_goals_status, get_calories
from app.api.trainings_info.crud import get_user_trainings, post_user_training
from app.api.trainings_info.models import Dashboard, Exercise


async def get_user_training_metrics(
    user_id: str,
    request: Request,
    start_date: str | None = None,
    end_date: str | None = None,
):
    dashboard = Dashboard(time="00:00:00", distance=0.0, milestones=0, calories=0)
    trainings = await get_user_trainings(
        user_id=user_id, request=request, end_date=end_date, start_date=start_date
    )

    if trainings is None:
        return dashboard

    goals = await get_user_goals(user_id=user_id, request=request)

    if goals is not None:
        goals_status = update_goals_status(goals=goals, trainings=trainings)
        for goal in goals_status["goals"]:
            if goal["completed"]:
                dashboard.milestones += 1

    for training in trainings:
        for exercise in training["exercises"]:
            dashboard.calories += get_calories(
                exercise_type=exercise["exercise_type"],
                total_time=exercise["time"],
            )
            hours, minutes, seconds = map(int, exercise["time"].split(":"))
            time_obj = datetime.time(hours, minutes, seconds)
            total_seconds = (
                time_obj.hour * 3600
                + time_obj.minute * 60
                + time_obj.second
                + dashboard.time.hour * 3600
                + dashboard.time.minute * 60
                + dashboard.time.second
            )

            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            result_time = datetime.time(hours, minutes, seconds)
            dashboard.time = result_time
            dashboard.distance += exercise["steps"] * 0.75

    return dashboard


async def load_user_training(
    user_id: str, exercises: list[Exercise], training_id: str, request: Request
):
    new_training = await post_user_training(
        user_id=user_id, exercises=exercises, training_id=training_id, request=request
    )
    return new_training
