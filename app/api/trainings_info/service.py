import datetime
from fastapi import Request
import httpx
from app.api.goals.crud import get_user_goals
from app.api.goals.service import update_goals_status, get_calories, get_user_weigth
from app.api.trainings_info.crud import (
    get_user_trainings,
    post_user_training,
    get_trainings_by_id,
)
from app.api.trainings_info.models import Dashboard, Exercise
from app.config.config import METRICS_SERVICE_URL
from app.config.config import logger


async def get_user_training_metrics(
    user_id: str,
    request: Request,
    start_date: str | None = None,
    end_date: str | None = None,
):
    dashboard = Dashboard(time="00:00:00", distance=0.0, milestones=0, calories=0)
    logger.info("Starting to caclulate training metrics", user=user_id)
    trainings = await get_user_trainings(
        user_id=user_id, request=request, end_date=end_date, start_date=start_date
    )

    if trainings is None:
        logger.info("Trainings not found", user=user_id)
        return dashboard

    goals = await get_user_goals(user_id=user_id, request=request)

    weigth = get_user_weigth(user_id=user_id)
    logger.info("Weigth", user=user_id, weight=weigth)

    if goals is not None:
        goals_status = update_goals_status(
            goals=goals, trainings=trainings, weigth=weigth
        )
        for goal in goals_status["goals"]:
            if goal["completed"]:
                dashboard.milestones += 1

    logger.info("Calculating calories, time and distance", user=user_id)
    for training in trainings:
        for exercise in training["exercises"]:
            dashboard.calories += get_calories(
                exercise_type=exercise["exercise_type"],
                total_time=exercise["time"],
                weigth=weigth,
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

    # Check enviroment variable
    if METRICS_SERVICE_URL != "":
        logger.info("Reaching metrics service", user=user_id)
        trainings = await get_trainings_by_id(training_id=training_id, request=request)
        metrics = {
            "metric": {
                "metric_type": "usage",
                "completed_counter": 0,
                "fulfilled_counter": 0,
            }
        }

        for training in trainings:
            completed = True
            for exercise in training["exercises"]:
                if exercise["finished"] is False:
                    completed = False
            metrics["metric"]["fulfilled_counter"] += 1
            metrics["metric"]["completed_counter"] += int(completed)
        # Update metric
        logger.info("Reaching metrics service", user=user_id, request=metrics)
        url = METRICS_SERVICE_URL + "metrics/trainings/" + training_id
        response = httpx.put(url, json=metrics)
        if response.status_code not in [200, 201]:
            logger.error(
                "Metrics service error", user=user_id, status_code=response.status_code
            )

    return new_training
