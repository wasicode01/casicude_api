from pydantic import BaseModel

class RoutineBase(BaseModel):
    name: str
    state: bool   # ahora es booleano

class RoutineCreate(RoutineBase):
    pass

class Routine(RoutineBase):
    id: int

    class Config:
        orm_mode = True