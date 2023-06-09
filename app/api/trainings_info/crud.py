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
