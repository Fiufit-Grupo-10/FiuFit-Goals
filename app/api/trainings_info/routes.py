from fastapi import APIRouter, HTTPException, Request
from app.api.trainings_info import crud, service
from app.api.trainings_info.models import Exercise, Training, Dashboard


router = APIRouter(tags=["training"])


@router.post("/users/{user_id}/training", response_model=Training, status_code=201)
async def load_training(user_id: str, exercises: list[Exercise], request: Request):
    new_training = await crud.load_user_training(
        user_id=user_id, exercises=exercises, request=request
    )
    return new_training


@router.get("/users/{user_id}/training", response_model=list[Training], status_code=200)
async def get_trainings(user_id: str, request: Request):
    new_training = await crud.get_user_trainings(user_id=user_id, request=request)
    if new_training is None:
        raise HTTPException(status_code=404, detail=f"{user_id} trainings not found")
    return new_training


@router.get(
    "/users/{user_id}/training/metrics", response_model=Dashboard, status_code=200
)
async def get_trainings_metrics(user_id: str, request: Request):
    panel = await service.get_user_training_metrics(user_id=user_id, request=request)
    return panel
