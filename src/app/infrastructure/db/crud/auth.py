"""
CRUD relacionado con autenticación y gestión de usuarios.

Contiene funciones para registrar usuarios y validar credenciales.
"""

from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.domain.models.user import UserCreate
from app.infrastructure.db.models.user import UserModel


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(db: Session, user: UserCreate):
    """Registra un nuevo usuario en la base de datos."""
    hashed_password = pwd_context.hash(user.password)
    db_user = UserModel(
        username=user.username, email=user.email, password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, username: str, password: str):
    """Valida las credenciales de un usuario."""
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if not db_user or not pwd_context.verify(password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return db_user
