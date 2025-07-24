"""
Router de autenticación.

Define endpoints para registro y login de usuarios, incluyendo
generación de tokens JWT y manejo de errores.
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.infrastructure.db.session import get_db
from app.domain.models.user import UserCreate
from app.infrastructure.db.crud.auth import register_user, authenticate_user
from app.core.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])
logger = logging.getLogger(__name__)


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario con contraseña hasheada.

    Args:
        user (UserCreate): Datos del usuario.
        db (Session): Sesión de base de datos.

    Returns:
        dict: Mensaje de éxito.
    """
    try:
        register_user(db=db, user=user)
        return {"msg": "User created"}
    except Exception as e:
        logger.error("Error registering user: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.post("/login")
def login(
    username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)
):
    """
    Autentica un usuario y devuelve un token JWT.

    Args:
        username (str): Nombre de usuario.
        password (str): Contraseña.
        db (Session): Sesión de base de datos.

    Returns:
        dict: Token de acceso y tipo.
    """
    try:
        user = authenticate_user(db, username, password)
        token = create_access_token({"sub": str(user.id)})
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error("Error during login: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
