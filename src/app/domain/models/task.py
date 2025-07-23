from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_done: bool = False
    priority: Optional[str] = None
    assignee: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True


class TaskListWithCompletion(BaseModel):
    tasks: List[Task]
    completion_percentage: float
