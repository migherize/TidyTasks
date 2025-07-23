"""
Modelos Pydantic para la gestión de listas de tareas.
"""

from typing import List

from pydantic import BaseModel, Field, field_validator

from app.domain.models.task import Task


class TaskListBase(BaseModel):
    """
    Modelo base para listas de tareas con validación de nombre.
    """

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nombre de la lista de tareas (3-50 caracteres)",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """Valida que el nombre no esté vacío ni solo contenga espacios."""
        if not value.strip():
            raise ValueError("El nombre no puede estar vacío o solo contener espacios")
        return value


class TaskListCreate(TaskListBase):
    """
    Modelo de entrada para crear una nueva lista de tareas
    """


class TaskList(TaskListBase):
    """
    Modelo de respuesta para una lista de tareas
    """

    id: int
    tasks: List[Task] = []

    model_config = {"from_attributes": True}
