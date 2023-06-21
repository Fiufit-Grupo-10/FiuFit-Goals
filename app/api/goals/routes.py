from fastapi import APIRouter, HTTPException, Request, status
from app.api.goals import service
from app.api.goals.models import Goal, UserGoalsReturn

router = APIRouter(tags=["goals"])


@router.post(
    "/users/{user_id}/goals",
    response_model=UserGoalsReturn,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_goals(user_id: str, goals: list[Goal], request: Request):
    try:
        new_goals = await service.create_user_goals(
            user_id=user_id, goals=goals, request=request
        )
        return new_goals
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{user_id} goals already exist",
        )


@router.put(
    "/users/{user_id}/goals",
    response_model=UserGoalsReturn,
    status_code=status.HTTP_200_OK,
)
async def update_user_goals(user_id: str, goals: list[Goal], request: Request):
    updated_goals = await service.update_user_goals(
        user_id=user_id, goals=goals, request=request
    )
    if updated_goals is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{user_id} goals not found"
        )
    return updated_goals


@router.get(
    "/users/{user_id}/goals",
    response_model=UserGoalsReturn,
    status_code=status.HTTP_200_OK,
)
async def get_user_goals(user_id: str, request: Request):
    goals = await service.get_user_goals(user_id=user_id, request=request)
    if goals is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{user_id} goals not found"
        )
    return goals
