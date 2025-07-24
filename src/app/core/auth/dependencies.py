"""
Dependencia para obtener el usuario autenticado a partir de un token JWT.

Este módulo utiliza OAuth2 con `Bearer Token` para extraer el token del encabezado
y verifica su validez utilizando `verify_token`. Si el token es válido y el usuario
existe en la base de datos, se retorna el usuario; de lo contrario, lanza un error 401.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.auth.jwt import verify_token
from app.infrastructure.db.session import get_db
from app.infrastructure.db.models.user import UserModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    """
    Extrae y valida el token JWT, y retorna el usuario correspondiente.

    Args:
        token (str): Token JWT extraído automáticamente desde el header `Authorization`.
        db (Session): Sesión de base de datos inyectada con dependencia.

    Raises:
        HTTPException: Si el token es inválido o el usuario no existe.

    Returns:
        UserModel: Instancia del usuario autenticado.
    """
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado"
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: sin ID de usuario",
        )

    try:
        user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al consultar el usuario en la base de datos",
        ) from e

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado"
        )

    return user
