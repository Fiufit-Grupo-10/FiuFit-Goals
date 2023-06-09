from fastapi import Request
from fastapi.encoders import jsonable_encoder
from app.api.goals.models import Goal, UserGoals
from app.config.database import GOALS_COLLECTION_NAME


async def create_user_goals(user_id: str, goals: list[Goal], request: Request):
    goals = UserGoals(user_id=user_id, goals=goals)
    goals = jsonable_encoder(goals)
    new_goals = await request.app.mongodb[GOALS_COLLECTION_NAME].insert_one(goals)
    created_goals = await request.app.mongodb[GOALS_COLLECTION_NAME].find_one(
        {"_id": new_goals.inserted_id}
    )
    return created_goals


async def update_user_goals(user_id: str, goals: list[Goal], request: Request):
    old_goals = await request.app.mongodb[GOALS_COLLECTION_NAME].find_one(
        {"user_id": user_id}
    )
    if old_goals is None:
        return None

    old_goals["goals"] = goals
    old_goals = jsonable_encoder(old_goals)
    await request.app.mongodb[GOALS_COLLECTION_NAME].delete_one(
        {"_id": old_goals["_id"]}
    )
    new_goals = await request.app.mongodb[GOALS_COLLECTION_NAME].insert_one(old_goals)
    updated_goals = await request.app.mongodb[GOALS_COLLECTION_NAME].find_one(
        {"_id": new_goals.inserted_id}
    )
    return updated_goals


async def get_user_goals(user_id: str, request: Request):
    goals = await request.app.mongodb[GOALS_COLLECTION_NAME].find_one(
        {"user_id": user_id}
    )
    return goals
