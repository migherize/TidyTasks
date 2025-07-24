"""
Esquemas de Pydantic para listas de tareas (Task Lists) en TidyTasks.
Define modelos para respuestas y solicitudes relacionadas con listas de tareas.
"""

from typing import List, Optional

from pydantic import BaseModel, Field, field_validator
from app.api.schemas.task import TaskResponse
from app.core.constants import ColorTagEnum


class TaskListResponse(BaseModel):
    """
    Esquema de respuesta que representa una lista de tareas.
    """

    id: int
    name: str
    color_tag: Optional[str] = None
    category: Optional[str] = None
    tasks: List[TaskResponse] = []

    model_config = {"from_attributes": True}


class TaskListWithCompletionResponse(BaseModel):
    """
    Esquema de respuesta que incluye el porcentaje de completitud de una lista de tareas.
    """

    tasks: List[TaskResponse]
    completion_percentage: float

    model_config = {"from_attributes": True}


class TaskListRequest(BaseModel):
    """
    Esquema para la solicitud de creación de una nueva lista de tareas.
    """

    name: str = Field(..., min_length=3, max_length=50)
    color_tag: Optional[ColorTagEnum] = None
    category: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        """
        Validador para asegurarse de que el nombre no esté vacío ni solo contenga espacios.
        """
        value = value.strip()
        if not value:
            raise ValueError("El nombre no puede estar vacío o solo con espacios.")
        return value
