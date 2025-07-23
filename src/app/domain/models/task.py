from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from app.core.constants import PriorityLevel
import re


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Título de la tarea")
    description: Optional[str] = Field(None, max_length=500, description="Descripción de la tarea")
    is_done: bool = Field(default=False, description="¿Está completada?")
    priority: Optional[PriorityLevel] = Field(None, description="Prioridad: low, medium o high")
    assignee_to: Optional[str] = Field(None, description="Persona asignada (correo electrónico)")

    @field_validator("title")
    def title_not_empty(cls, value):
        if not value.strip():
            raise ValueError("El título no puede estar vacío")
        return value

    @field_validator("assignee_to")
    def assignee_format(cls, value):
        if value and not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise ValueError("El campo 'assignee' debe ser un email válido")
        return value


class TaskCreate(TaskBase):
    """
    Modelo para crear una tarea.
    """
    pass


class TaskUpdate(TaskBase):
    """
    Modelo para actualizar una tarea existente.
    """
    pass


class Task(TaskBase):
    """
    Modelo de respuesta de una tarea.
    """
    id: int

    model_config = {
        "from_attributes": True
    }
