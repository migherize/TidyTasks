from fastapi import APIRouter
from app.domain.models.task_list import TaskListCreate, TaskList

router = APIRouter(prefix="/lists", tags=["Task Lists"])

@router.post("/", response_model=TaskList)
def create_list(list: TaskListCreate):
    pass

@router.get("/{list_id}", response_model=TaskList)
def get_list(list_id: int):
   pass

@router.put("/{list_id}", response_model=TaskList)
def update_list(list_id: int, list: TaskListCreate):
   pass

@router.delete("/{list_id}", status_code=204)
def delete_list(list_id: int):
   pass
