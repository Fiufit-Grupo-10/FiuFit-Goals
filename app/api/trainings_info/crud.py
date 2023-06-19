from fastapi import Request
from fastapi.encoders import jsonable_encoder
from app.api.trainings_info.models import Exercise, Training
from app.config.database import TRAININGS_COLLECTION_NAME


async def load_user_training(user_id: str, exercises: list[Exercise], request: Request):
    training = Training(user_id=user_id, exercises=exercises)
    training = jsonable_encoder(training)
    new_training = await request.app.mongodb[TRAININGS_COLLECTION_NAME].insert_one(
        training
    )
    created_training = await request.app.mongodb[TRAININGS_COLLECTION_NAME].find_one(
        {"_id": new_training.inserted_id}
    )
    return created_training


async def get_user_trainings(
    user_id: str,
    request: Request,
    start_date: str | None = None,
    end_date: str | None = None,
):
    query = {"user_id": user_id}
    if start_date is not None and end_date is not None:
        query["updated"] = {"$lte": end_date, "$gte": start_date}
    trainings = [
        training
        async for training in request.app.mongodb[TRAININGS_COLLECTION_NAME].find(
            filter=query
        )
    ]
    if len(trainings) == 0:
        return None
    return trainings
