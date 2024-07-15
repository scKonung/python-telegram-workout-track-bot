from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from workout_tracker.db.database import Base

class TrainingPlan(Base):
    __tablename__ = 'training_plan'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, unique=False, nullable=True)
    user_id = Column(Integer, unique=False, nullable=False)

    exercise_plans = relationship("ExercisePlan", back_populates="training_plan")

class ExercisePlan(Base):
    __tablename__ = 'exercise_plan'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, unique=False, nullable=False)
    training_id = Column(Integer,ForeignKey("training_plan.id"), nullable=False)
    worm_up_sets = Column(Integer, unique=False, nullable=True)
    working_sets = Column(Integer, unique=False, nullable=False)

    training_plan = relationship("TrainingPlan", back_populates="exercise_plans")