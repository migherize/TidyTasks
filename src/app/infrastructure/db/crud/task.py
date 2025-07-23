from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.domain.models.task import TaskCreate, TaskUpdate
from app.infrastructure.db.models.task import TaskModel
from app.infrastructure.db.models.task_list import TaskListModel


def create_task(db: Session, list_id: int, task_data: TaskCreate) -> TaskModel:
    task_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
    if not task_list:
        raise HTTPException(status_code=404, detail="Task list not found")

    db_task = TaskModel(**task_data.dict(), list_id=list_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, list_id: int, task_id: int) -> TaskModel:
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.list_id == list_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def update_task(db: Session, list_id: int, task_id: int, task_data: TaskUpdate) -> TaskModel:
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.list_id == list_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, list_id: int, task_id: int) -> None:
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.list_id == list_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()

def update_task_status(db: Session, list_id: int, task_id: int, is_done: bool) -> TaskModel | None:
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.list_id == list_id).first()
    if not task:
        return None
    task.is_done = is_done
    db.commit()
    db.refresh(task)
    return task
