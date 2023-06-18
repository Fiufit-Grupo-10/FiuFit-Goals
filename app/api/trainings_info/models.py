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
    updated: datetime = Field(default_factory=datetime.utcnow)

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
            }
        }


class Training(BaseModel):
    id: str = Field(default_factory=uuid4, alias="_id")
    user_id: str = Field(...)
    exercises: list[Exercise]
    
class Dashboard(BaseModel):
    distance: float 
    time: time 
    calories: float 
    milestones: int 
    
