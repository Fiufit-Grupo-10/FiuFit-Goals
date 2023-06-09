from fastapi import APIRouter, Request
from app.api.trainings_info import crud
from app.api.trainings_info.models import Exercise, Training


router = APIRouter(tags=["training"])


@router.post("/users/{user_id}/training", response_model=Training, status_code=201)
async def load_training_info(user_id: str, exercises: list[Exercise], request: Request):
    new_training = await crud.load_user_training(
        user_id=user_id, exercises=exercises, request=request
    )
    return new_training
