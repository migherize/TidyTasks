from fastapi import APIRouter
from app.domain.models.task import Task, TaskCreate, TaskUpdate

router = APIRouter(prefix="/lists/{list_id}/tasks", tags=["Tasks"])

@router.post("/", response_model=Task)
def create_task(list_id: int, task: TaskCreate):
    pass

@router.get("/{task_id}", response_model=Task)
def get_task(list_id: int, task_id: int):
    pass

@router.put("/{task_id}", response_model=Task)
def update_task(list_id: int, task_id: int, task: TaskUpdate):
    pass

@router.delete("/{task_id}", status_code=204)
def delete_task(list_id: int, task_id: int):
    pass
