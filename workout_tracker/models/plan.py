from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from workout_tracker.db.database import Base

class TrainingPlan(Base):
    __tablename__ = 'training_plans'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, unique=False, nullable=False)

    exercises = relationship("ExercisePlan", back_populates="training_plan")

class ExercisePlan(Base):
    __tablename__ = 'exercise_plans'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, unique=False, nullable=False)
    training_id = Column(Integer,ForeignKey("training_plans.id"), nullable=False)
    worm_up_sets = Column(Integer, unique=False, nullable=True)
    working_sets = Column(Integer, unique=False, nullable=False)