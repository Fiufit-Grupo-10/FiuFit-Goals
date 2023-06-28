from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime, time


class Exercise(BaseModel):
    name: str
    category: str
    amount: int
    exercise_type: str
    finished: bool
    time: time
    steps: int

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "flexiones",
                "category": "repeticiones",
                "amount": "20",
                "exercise_type": "Fuerza",
                "finished": True,
                "time": "01:10:15",
                "steps": 50,
            }
        }


class ExerciseRequest(BaseModel):
    training_id: str = Field(...)
    exercises: list[Exercise]


class Training(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    user_id: str = Field(...)
    training_id: str = Field(...)
    exercises: list[Exercise]
    updated: datetime = Field(default_factory=datetime.utcnow)


class Dashboard(BaseModel):
    distance: float = Field(description="Distance in meters")
    time: time
    calories: float
    milestones: int
