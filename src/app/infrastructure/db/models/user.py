"""
Modelo ORM para la tabla de usuarios en la base de datos.

Define la estructura de la tabla `users` con sus columnas y restricciones.
"""

from sqlalchemy import Column, Integer, String
from app.infrastructure.db.base import Base


class UserModel(Base):
    """
    Representa un usuario registrado en el sistema.

    Atributos:
        id (int): Identificador único del usuario.
        username (str): Nombre de usuario único y no nulo.
        email (str): Correo electrónico único y no nulo.
        password_hash (str): Hash de la contraseña del usuario.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def __repr__(self):
        """
        Devuelve una representación en cadena legible del objeto UserModel.

        Útil para depuración y logging.

        Returns:
            str: Representación en formato <User(id=..., username=...)>
        """
        return f"<User(id={self.id}, username={self.username})>"

    def to_dict(self):
        """
        Convierte el objeto UserModel en un diccionario con campos seleccionados.

        Returns:
            dict: Diccionario con claves 'id', 'username' y 'email'.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }
