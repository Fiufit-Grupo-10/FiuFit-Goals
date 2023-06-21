from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4


class GoalType(str, Enum):
    points = "points"
    calories = "calories"
    steps = "steps"


class Goal(BaseModel):
    title: str = Field(description="Title of the goal")
    training_type: str = Field(description="Training type of the goal")
    amount: int = Field(description="Amount of points/calories/steps of thje goal")
    goal_type: GoalType = Field(description="Goal type")
    limit: str = Field(description="Time limit of the goal")
    notified: bool = Field(
        description="Indicates wheter the user has been notified from this goal been achieved",
        default=False,
    )


class GoalReturn(Goal):
    percentage: float = Field(
        description="Indicates percentage of the goal achieved by the user", default=0.0
    )
    completed: bool = Field(
        description="Indicates wheter the usar has/has not completed the goal",
        default=False,
    )


class UserGoals(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    user_id: str = Field(...)
    goals: list[Goal]


class UserGoalsReturn(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    user_id: str = Field(...)
    goals: list[GoalReturn]
