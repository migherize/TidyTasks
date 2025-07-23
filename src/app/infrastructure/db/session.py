from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB = os.getenv("DB")
USERDB = os.getenv("USERDB")
PASSWORDDB = os.getenv("PASSWORDDB")
NAME_SERVICEDB = os.getenv("NAME_SERVICEDB")
PORT = os.getenv("PORT")
NAMEDB = os.getenv("NAMEDB")

DATABASE_URL = f"{DB}://{USERDB}:{PASSWORDDB}@{NAME_SERVICEDB}:{PORT}/{NAMEDB}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
