"""
Modelos Pydantic para la gestión de tareas.
"""

import re
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.core.constants import PriorityLevel


class TaskBase(BaseModel):
    """
    Modelo base para una tarea con validación de campos.
    """

    title: str = Field(
        ..., min_length=3, max_length=100, description="Título de la tarea"
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Descripción de la tarea"
    )
    is_done: bool = Field(default=False, description="¿Está completada?")
    priority: Optional[PriorityLevel] = Field(
        None, description="Prioridad: low, medium o high"
    )
    assigned_to: Optional[str] = Field(
        None, description="Persona asignada (correo electrónico)"
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value: str) -> str:
        """Valida que el título no esté vacío ni solo contenga espacios."""
        if not value.strip():
            raise ValueError("El título no puede estar vacío")
        return value

    @field_validator("assigned_to")
    @classmethod
    def assignee_format(cls, value: str) -> str:
        """Valida que el campo 'assigned_to' sea un email válido si no es None."""
        if value and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise ValueError("El campo 'assignee' debe ser un email válido")
        return value


class TaskCreate(TaskBase):
    """
    Modelo para crear una tarea.
    """


class TaskUpdate(TaskBase):
    """
    Modelo para actualizar una tarea existente.
    """


class Task(TaskBase):
    """
    Modelo de respuesta de una tarea.
    """

    id: int

    model_config = {"from_attributes": True}
