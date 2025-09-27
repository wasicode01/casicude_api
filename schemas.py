from pydantic import BaseModel
from datetime import date

class Group(BaseModel):
    id: int
    name: str
    description: str

class GroupCreate(BaseModel):
    name: str
    description: str

class Exercise(BaseModel):
    id: int
    group_id: int
    name: str
    sets: int
    reps: int
    weight: float
    date: date

class ExerciseCreate(BaseModel):
    group_id: int
    name: str
    sets: int
    reps: int
    weight: float
    date: date
