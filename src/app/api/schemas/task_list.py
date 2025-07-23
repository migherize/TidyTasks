from typing import List
from pydantic import BaseModel
from pydantic import BaseModel, Field, field_validator
from app.api.schemas.task import TaskResponse

class TaskListResponse(BaseModel):
    id: int
    name: str
    tasks: List[TaskResponse] = []

    model_config = {
        "from_attributes": True
    }

class TaskListWithCompletionResponse(BaseModel):
    tasks: List[TaskResponse]
    completion_percentage: float
    
    model_config = {
        "from_attributes": True
    }
class TaskListRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre no puede estar vacío o solo con espacios.")
        return value
