from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.domain.models.task import TaskCreate, TaskUpdate
from app.infrastructure.db.models.task import TaskModel
from app.infrastructure.db.models.task_list import TaskListModel
import logging

logger = logging.getLogger(__name__)


def create_task(db: Session, list_id: int, task_data: TaskCreate) -> TaskModel:
    """
    Crea una nueva tarea asociada a una lista específica.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista a la que se asignará la tarea.
        task_data (TaskCreate): Datos de la tarea a crear.

    Returns:
        TaskModel: Instancia de la tarea creada.

    Raises:
        HTTPException 404: Si la lista de tareas no existe.
        HTTPException 500: Si ocurre un error al crear la tarea.
    """
    try:
        task_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
        if not task_list:
            raise HTTPException(status_code=404, detail="Task list not found")

        logger.info(f"Creating task in list {list_id}: {task_data.dict()}")
        db_task = TaskModel(**task_data.dict(), list_id=list_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Failed to create task")


def get_task(db: Session, list_id: int, task_id: int) -> TaskModel:
    """
    Obtiene una tarea específica por su ID y el ID de su lista.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista que contiene la tarea.
        task_id (int): ID de la tarea a obtener.

    Returns:
        TaskModel: Instancia de la tarea encontrada.

    Raises:
        HTTPException 404: Si la tarea no existe.
        HTTPException 500: Si ocurre un error al obtener la tarea.
    """
    try:
        task = (
            db.query(TaskModel)
            .filter(TaskModel.id == task_id, TaskModel.list_id == list_id)
            .first()
        )
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except Exception as e:
        logger.error(f"Error fetching task {task_id} from list {list_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch task")


def update_task(
    db: Session, list_id: int, task_id: int, task_data: TaskUpdate
) -> TaskModel:
    """
    Actualiza parcialmente una tarea existente.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista que contiene la tarea.
        task_id (int): ID de la tarea a actualizar.
        task_data (TaskUpdate): Campos para actualizar en la tarea.

    Returns:
        TaskModel: Instancia de la tarea actualizada.

    Raises:
        HTTPException 404: Si la tarea no existe.
        HTTPException 500: Si ocurre un error al actualizar la tarea.
    """
    try:
        db_task = (
            db.query(TaskModel)
            .filter(TaskModel.id == task_id, TaskModel.list_id == list_id)
            .first()
        )
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")

        logger.info(
            f"Updating task {task_id} in list {list_id} with data: {task_data.dict(exclude_unset=True)}"
        )
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        logger.error(f"Error updating task {task_id} in list {list_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update task")


def delete_task(db: Session, list_id: int, task_id: int) -> None:
    """
    Elimina una tarea específica por su ID y lista asociada.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista que contiene la tarea.
        task_id (int): ID de la tarea a eliminar.

    Raises:
        HTTPException 404: Si la tarea no existe.
        HTTPException 500: Si ocurre un error al eliminar la tarea.
    """
    try:
        db_task = (
            db.query(TaskModel)
            .filter(TaskModel.id == task_id, TaskModel.list_id == list_id)
            .first()
        )
        if not db_task:
            return False  # No encontrada
        logger.info(f"Deleting task {task_id} from list {list_id}")
        db.delete(db_task)
        db.commit()
        return True
    except Exception as e:
        logger.error(f"Error deleting task {task_id} from list {list_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete task")


def update_task_status(
    db: Session, list_id: int, task_id: int, is_done: bool
) -> TaskModel:
    """
    Cambia el estado de completitud de una tarea.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista que contiene la tarea.
        task_id (int): ID de la tarea a modificar.
        is_done (bool): Nuevo estado de completitud.

    Returns:
        TaskModel: Instancia de la tarea actualizada.

    Raises:
        HTTPException 404: Si la tarea no existe.
        HTTPException 500: Si ocurre un error al actualizar el estado.
    """
    try:
        task = (
            db.query(TaskModel)
            .filter(TaskModel.id == task_id, TaskModel.list_id == list_id)
            .first()
        )
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        logger.info(f"Updating status of task {task_id} in list {list_id} to {is_done}")
        task.is_done = is_done
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        logger.error(f"Error updating status for task {task_id} in list {list_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update task status")
