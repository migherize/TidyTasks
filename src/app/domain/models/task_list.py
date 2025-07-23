from pydantic import BaseModel, Field, field_validator
from typing import List
from app.domain.models.task import Task

class TaskListBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nombre de la lista de tareas (3-50 caracteres)")

    @field_validator("name")
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío o solo contener espacios")
        return v

class TaskListCreate(TaskListBase):
    """
    Modelo de entrada para crear una nueva lista de tareas
    """
    pass

class TaskList(TaskListBase):
    """
    Modelo de respuesta para una lista de tareas
    """
    id: int
    tasks: List[Task] = []

    model_config = {
        "from_attributes": True
    }
