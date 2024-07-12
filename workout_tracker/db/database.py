from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from workout_tracker.constans import DATABASE_URL



_engine = create_engine(DATABASE_URL)
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
Base = declarative_base()
db = _SessionLocal()


def init_db():
    from workout_tracker.models import plan
    Base.metadata.create_all(bind=_engine)
