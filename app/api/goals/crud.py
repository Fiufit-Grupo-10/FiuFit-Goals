from fastapi import Request
from fastapi.encoders import jsonable_encoder
from app.api.goals.models import Goal, UserGoals
from app.config.database import GOALS_COLLECTION_NAME


async def create_user_goals(user_id: str,goals: list[Goal], request: Request):
    goals = UserGoals(user_id=user_id,goals=goals)
    goals = jsonable_encoder(goals)
    new_goals = await request.app.mongodb[GOALS_COLLECTION_NAME].insert_one(goals)
    created_goals = await request.app.mongodb[GOALS_COLLECTION_NAME].find_one(
        {"_id": new_goals.inserted_id}
    )
    return created_goals

