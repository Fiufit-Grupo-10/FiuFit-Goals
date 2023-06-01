from enum import Enum
from pydantic import BaseModel, Field
from uuid import uuid4

MAX_TITLE_LENGTH = 200
MIN_TITLE_LENGTH = 3
MAX_DESCRIPTION_LENGTH = 5000


class GoalType(str, Enum):
    steps = "steps"
    calories = "calories"
    points = "points"


class Goal(BaseModel):
    training_type: str = Field(...)
    amount: int = Field(...)
    goal_type: GoalType                  

class UserGoals(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    user_id : str = Field(...)
    goals: list[Goal]



