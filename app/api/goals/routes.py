from fastapi import APIRouter, HTTPException, Request
from app.api.goals import crud
from app.api.goals.models import Goal, UserGoals

router = APIRouter(tags=["goals"])


@router.post("/users/{user_id}/goals", response_model=UserGoals, status_code=201)
async def create_user_goals(user_id: str, goals: list[Goal], request: Request):
    new_goals = await crud.create_user_goals(
        user_id=user_id, goals=goals, request=request
    )
    return new_goals


@router.put("/users/{user_id}/goals", response_model=UserGoals, status_code=200)
async def update_user_goals(user_id: str, goals: list[Goal], request: Request):
    updated_goals = await crud.update_user_goals(
        user_id=user_id, goals=goals, request=request
    )
    if updated_goals is None:
        raise HTTPException(status_code=404, detail=f"{user_id} goals not found")
    return updated_goals


@router.get("/users/{user_id}/goals", response_model=UserGoals, status_code=200)
async def get_user_goals(user_id: str, request: Request):
    goals = await crud.get_user_goals(user_id=user_id, request=request)
    if goals is None:
        raise HTTPException(status_code=404, detail=f"{user_id} goals not found")
    return goals
