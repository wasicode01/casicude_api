from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class RoutineBase(BaseModel):
    name: str
    state: bool   # ahora es booleano


class RoutineCreate(RoutineBase):
    pass


class Routine(RoutineBase):
    id: int

    class Config:
        orm_mode = True


class ExerciseRepetitionBase(BaseModel):
    exercise_id: int
    routine_id: Optional[int] = None
    num_reps: int
    weight: float = 0.0
    notes: Optional[str] = None


class ExerciseRepetitionCreate(ExerciseRepetitionBase):
    pass


class ExerciseRepetition(ExerciseRepetitionBase):
    id: int
    performed_at: datetime

    class Config:
        orm_mode = True


# --- Auth schemas ---
class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None