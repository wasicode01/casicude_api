from sqlalchemy import Column, Integer, String, Boolean, Table, ForeignKey, BigInteger, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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
    repetitions = relationship("ExerciseRepetition", back_populates="exercise")


class ExerciseRepetition(Base):
    __tablename__ = "exercise_repetitions"
    
    id = Column(BigInteger, primary_key=True, index=True)
    exercise_id = Column(Integer, ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False)
    routine_id = Column(Integer, ForeignKey("routine.id", ondelete="SET NULL"), nullable=True)
    num_reps = Column(Integer, nullable=False)
    weight = Column(Numeric(8, 2), default=0.00)
    performed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(Text)
    
    # Relaciones
    exercise = relationship("Exercise", back_populates="repetitions")
    routine = relationship("Routine")


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)