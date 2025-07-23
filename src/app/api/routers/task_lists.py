from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import Query
from app.domain.models.task import TaskListWithCompletion
from app.domain.models.task_list import TaskListCreate, TaskList
from app.infrastructure.db.session import get_db
from app.infrastructure.db.crud.task_list import (
    create_task_list,
    get_task_list,
    update_task_list,
    delete_task_list,
    get_tasks_with_filters
)

router = APIRouter(prefix="/lists", tags=["Task Lists"])

@router.post("/", response_model=TaskList, status_code=status.HTTP_201_CREATED)
def create_list(list_data: TaskListCreate, db: Session = Depends(get_db)):
    return create_task_list(db, list_data)

@router.get("/{list_id}", response_model=TaskList)
def get_list(list_id: int, db: Session = Depends(get_db)):
    return get_task_list(db, list_id)

@router.put("/{list_id}", response_model=TaskList)
def update_list(list_id: int, list_data: TaskListCreate, db: Session = Depends(get_db)):
    return update_task_list(db, list_id, list_data)

@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_list(list_id: int, db: Session = Depends(get_db)):
    delete_task_list(db, list_id)

@router.get("/", response_model=TaskListWithCompletion)
def list_tasks(
    list_id: int,
    is_done: Optional[bool] = Query(None, description="Filter by task done status"),
    priority: Optional[str] = Query(None, description="Filter by task priority"),
    db: Session = Depends(get_db)
):
    tasks, percentage = get_tasks_with_filters(db, list_id, is_done, priority)
    return {"tasks": tasks, "completion_percentage": percentage}
