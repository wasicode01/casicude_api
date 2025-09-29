from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Routine(Base):
    __tablename__ = "routine"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    state = Column(Boolean, nullable=False, default=True)