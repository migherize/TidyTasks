from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status
from app.domain.models.task_list import TaskListCreate
from app.infrastructure.db.models.task_list import TaskListModel
from app.infrastructure.db.models.task import TaskModel
import logging

logger = logging.getLogger(__name__)

def create_task_list(db: Session, list_data: TaskListCreate) -> TaskListModel:
    logger.info(f"Creating task list: {list_data.dict()}")
    db_list = TaskListModel(**list_data.dict())
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

def get_task_list(db: Session, list_id: int) -> TaskListModel:
    logger.info(f"Getting task list ID: {list_id}")
    db_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
    if not db_list:
        logger.warning(f"Task list {list_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    return db_list

def update_task_list(db: Session, list_id: int, list_data: TaskListCreate) -> TaskListModel:
    logger.info(f"Updating task list ID {list_id} with: {list_data.dict()}")
    db_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
    if not db_list:
        logger.warning(f"Task list {list_id} not found for update")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    for key, value in list_data.dict().items():
        setattr(db_list, key, value)
    db.commit()
    db.refresh(db_list)
    return db_list

def delete_task_list(db: Session, list_id: int) -> None:
    logger.info(f"Deleting task list ID: {list_id}")
    db_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
    if not db_list:
        logger.warning(f"Task list {list_id} not found for deletion")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="List not found")
    db.delete(db_list)
    db.commit()

def get_tasks_with_filters(db: Session, list_id: int, is_done: Optional[bool], priority: Optional[str]) -> list[TaskModel]:
    query = db.query(TaskModel).filter(TaskModel.list_id == list_id)

    if is_done is not None:
        query = query.filter(TaskModel.is_done == is_done)
    if priority:
        query = query.filter(TaskModel.priority == priority)

    filtered_tasks = query.all()

    all_tasks = db.query(TaskModel).filter(TaskModel.list_id == list_id).all()
    total = len(all_tasks)
    done = len([task for task in all_tasks if task.is_done])
    percentage = round((done / total) * 100, 2) if total > 0 else 0.0

    return filtered_tasks, percentage