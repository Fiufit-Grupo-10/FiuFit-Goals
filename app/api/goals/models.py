from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4

MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MAX_DESCRIPTION_LENGTH = 5000


class GoalType(str, Enum):
    points = "points"
    calories = "calories"
    steps = "steps"    
    


class Goal(BaseModel):
    title: str = Field(...)
    training_type: str = Field(...)
    amount: int = Field(...)
    goal_type: GoalType
    limit: str


class GoalReturn(Goal):
    percentage: float = Field(
        description="Indicates percetage of the goal achieved by the user", default=0.0
    )
    completed: bool = Field(
        description="Indicates wheter the usar has/has not completed the goal",
        default=False,
    )


class UserGoals(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    user_id: str = Field(...)
    goals: list[GoalReturn]
