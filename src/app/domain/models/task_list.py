from pydantic import BaseModel
from typing import List

from app.domain.models.task import Task

class TaskListBase(BaseModel):
    name: str


class TaskListCreate(TaskListBase):
    pass


class TaskList(TaskListBase):
    id: int
    tasks: List[Task] = []

    model_config = {
        "from_attributes": True
    }
