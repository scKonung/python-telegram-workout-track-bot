from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    from workout_tracker.models import plan
    Base.metadata.create_all(bind=engine)
