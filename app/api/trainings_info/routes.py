from fastapi import APIRouter, HTTPException, Request, Query, status
from app.api.trainings_info import crud, service
from app.api.trainings_info.models import ExerciseRequest, Training, Dashboard


router = APIRouter(tags=["training"])


@router.post(
    "/users/{user_id}/training",
    response_model=Training,
    status_code=status.HTTP_201_CREATED,
)
async def load_training(user_id: str, exercises: ExerciseRequest, request: Request):
    new_training = await service.load_user_training(
        user_id=user_id,
        exercises=exercises.exercises,
        training_id=exercises.training_id,
        request=request,
    )
    return new_training


@router.get(
    "/users/{user_id}/training",
    response_model=list[Training],
    status_code=status.HTTP_200_OK,
)
async def get_trainings(user_id: str, request: Request):
    new_training = await crud.get_user_trainings(user_id=user_id, request=request)
    if new_training is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{user_id} trainings not found",
        )
    return new_training


@router.get(
    "/users/{user_id}/training/metrics",
    response_model=Dashboard,
    status_code=status.HTTP_200_OK,
)
async def get_trainings_metrics(
    user_id: str,
    request: Request,
    start_date: str
    | None = Query(default=None, description="Start date in ISO format"),
    end_date: str | None = Query(default=None, description="End date in ISO format"),
):
    panel = await service.get_user_training_metrics(
        user_id=user_id, request=request, end_date=end_date, start_date=start_date
    )
    return panel
