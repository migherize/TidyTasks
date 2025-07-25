"""
Módulo de configuración de la base de datos para TidyTasks.

Este archivo define el motor de conexión a la base de datos y la dependencia `get_db`
utilizada por FastAPI para manejar sesiones con SQLAlchemy.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

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
    """
    Genera una sesión de base de datos para ser utilizada como dependencia en FastAPI.

    Cierra automáticamente la sesión una vez que la operación termina (usando `yield`).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
