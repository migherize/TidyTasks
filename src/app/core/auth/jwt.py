"""
Módulo de autenticación basado en JWT.

Este archivo proporciona funciones para:
- Crear tokens de acceso (`create_access_token`)
- Verificar y decodificar tokens (`verify_token`)

Usa el estándar JWT (JSON Web Token) con algoritmo HS256 para firmar y validar tokens.
La clave secreta y el tiempo de expiración se configuran mediante variables de entorno.
"""

import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_unsafe_secret")
ALGORITHM = "HS256"
access_token_exp = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_exp) if access_token_exp else 30


def create_access_token(data: dict) -> str:
    """
    Crea un token JWT firmado con clave secreta y expiración.

    Args:
        data (dict): Información a codificar en el token.

    Returns:
        str: Token JWT generado.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict | None:
    """
    Verifica la validez del token JWT y devuelve su contenido.

    Args:
        token (str): Token JWT a validar.

    Returns:
        dict | None: Payload decodificado si el token es válido, None si no lo es.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
