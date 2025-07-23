"""
Esquemas Pydantic para crear, actualizar y representar tareas en TidyTasks.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.constants import PriorityLevel


class TaskBase(BaseModel):
    """Esquema base con campos comunes para tareas."""

    title: str = Field(
        ..., min_length=1, max_length=200, description="Título de la tarea"
    )
    description: Optional[str] = Field(
        None, max_length=1000, description="Descripción de la tarea"
    )
    priority: PriorityLevel = Field(
        default=PriorityLevel.MEDIUM, description="Prioridad de la tarea"
    )
    assigned_to: Optional[UUID] = Field(None, description="UUID del usuario asignado")


class TaskCreate(TaskBase):
    """Request para crear una tarea"""


class TaskUpdate(BaseModel):
    """Request para actualizar parcialmente una tarea"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[PriorityLevel]
    assigned_to: Optional[UUID]
    is_done: Optional[bool]


class TaskResponse(TaskBase):
    """Response al obtener una tarea"""

    id: int
    is_done: bool
    assigned_to: Optional[UUID]
    list_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class StatusChangeRequest(BaseModel):
    """Request para cambiar estado de tarea"""

    is_done: bool = Field(..., description="Nuevo estado (completada o no)")
