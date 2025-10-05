from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

routine_exercise = Table(
    "routine_exercise",
    Base.metadata,
    Column("routine_id", Integer, ForeignKey("routine.id")),
    Column("exercise_id", Integer, ForeignKey("exercise.id"))
)

class Routine(Base):
    __tablename__ = "routine"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    state = Column(Boolean, nullable=False, default=True)
    exercises = relationship("Exercise", secondary=routine_exercise, back_populates="routines")



class Exercise(Base):
    __tablename__ = "exercise"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rest_time = Column(Integer)
    min_repetition = Column(Integer)
    max_repetition = Column(Integer)
    state = Column(Boolean)
    num_rep = Column(Integer)
    routines = relationship("Routine", secondary=routine_exercise, back_populates="exercises")