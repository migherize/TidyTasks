import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.domain.models.task import Task, TaskCreate, TaskUpdate
from app.infrastructure.db.session import get_db
from app.infrastructure.db.crud.task import create_task, get_task, update_task, delete_task

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lists/{list_id}/tasks", tags=["Tasks"])


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(list_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating task in list {list_id} with data: {task.dict()}")
    return create_task(db, list_id, task)


@router.get("/{task_id}", response_model=Task)
def get_task_endpoint(list_id: int, task_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching task {task_id} from list {list_id}")
    return get_task(db, list_id, task_id)


@router.put("/{task_id}", response_model=Task)
def update_task_endpoint(list_id: int, task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    logger.info(f"Updating task {task_id} in list {list_id} with data: {task.dict(exclude_unset=True)}")
    return update_task(db, list_id, task_id, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(list_id: int, task_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting task {task_id} from list {list_id}")
    delete_task(db, list_id, task_id)
