"""
Modelos Pydantic para operaciones relacionadas con usuarios.

"""

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """
    Esquema para la creación de un nuevo usuario.

    Atributos:
        username (str): Nombre de usuario único.
        email (EmailStr): Correo electrónico válido del usuario.
        password (str): Contraseña del usuario (no encriptada).
    """

    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Esquema para el inicio de sesión de un usuario.

    Atributos:
        username (str): Nombre de usuario registrado.
        password (str): Contraseña correspondiente al usuario.
    """

    username: str
    password: str


class UserOut(BaseModel):
    """
    Esquema de salida con los datos públicos del usuario.

    Atributos:
        id (int): Identificador único del usuario.
        username (str): Nombre de usuario.
        email (str): Correo electrónico del usuario.
    """

    id: int
    username: str
    email: str
