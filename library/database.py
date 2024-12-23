import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from library.models.base import Base
#from config import DATABASE_URL

DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()