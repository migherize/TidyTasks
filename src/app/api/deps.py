from fastapi import Depends
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_db

def get_db_session(db: Session = Depends(get_db)) -> Session:
    """
    Dependencia reutilizable para obtener una sesión de base de datos.
    """
    return db