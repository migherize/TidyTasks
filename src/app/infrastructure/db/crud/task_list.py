from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import HTTPException, status
from app.domain.models.task_list import TaskListCreate
from app.infrastructure.db.models.task_list import TaskListModel
from app.infrastructure.db.models.task import TaskModel
from app.domain.models.exceptions import TaskListCreationException
from app.core.constants import TaskListError
import logging

logger = logging.getLogger(__name__)


def create_task_list(db: Session, list_data: TaskListCreate) -> TaskListModel:
    """
    Crea una nueva lista de tareas en la base de datos.

    Args:
        db (Session): Sesión activa de base de datos.
        list_data (TaskListCreate): Datos para crear la lista de tareas.

    Returns:
        TaskListModel: La lista de tareas creada y persistida.

    Raises:
        TaskListCreationException: Si ocurre un error durante la creación.
    """
    try:
        logger.info(f"Creating task list: {list_data.dict()}")
        db_list = TaskListModel(**list_data.dict())
        db.add(db_list)
        db.commit()
        db.refresh(db_list)
        return db_list
    except Exception as e:
        logger.error(f"Error creating task list: {e}")
        raise TaskListCreationException(detail=TaskListError.CREATION_FAILED)


def get_task_list(db: Session, list_id: int) -> TaskListModel:
    """
    Obtiene una lista de tareas por su ID.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista a obtener.

    Returns:
        TaskListModel: La lista de tareas encontrada.

    Raises:
        HTTPException 404: Si la lista no existe.
        HTTPException 500: Si ocurre un error inesperado.
    """
    try:
        logger.info(f"Getting task list ID: {list_id}")
        db_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
        if not db_list:
            logger.warning(f"Task list {list_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
            )
        return db_list
    except Exception as e:
        logger.error(f"Error getting task list {list_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get task list")


def update_task_list(
    db: Session, list_id: int, list_data: TaskListCreate
) -> TaskListModel:
    """
    Actualiza una lista de tareas existente con nuevos datos.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista a actualizar.
        list_data (TaskListCreate): Nuevos datos para la lista.

    Returns:
        TaskListModel: La lista actualizada.

    Raises:
        HTTPException 404: Si la lista no existe.
        HTTPException 500: Si ocurre un error inesperado.
    """
    try:
        logger.info(f"Updating task list ID {list_id} with: {list_data.dict()}")
        db_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
        if not db_list:
            logger.warning(f"Task list {list_id} not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
            )
        for key, value in list_data.dict().items():
            setattr(db_list, key, value)
        db.commit()
        db.refresh(db_list)
        return db_list
    except Exception as e:
        logger.error(f"Error updating task list {list_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update task list")


def delete_task_list(db: Session, list_id: int) -> None:
    """
    Elimina una lista de tareas específica por su ID.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista a eliminar.

    Raises:
        HTTPException 404: Si la lista no existe.
        HTTPException 500: Si ocurre un error inesperado.
    """
    try:
        logger.info(f"Deleting task list ID: {list_id}")
        db_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
        if not db_list:
            logger.warning(f"Task list {list_id} not found for deletion")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
            )
        db.delete(db_list)
        db.commit()
    except Exception as e:
        logger.error(f"Error deleting task list {list_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete task list")


def get_tasks_with_filters(
    db: Session, list_id: int, is_done: Optional[bool], priority: Optional[str]
) -> tuple[list[TaskModel], float]:
    """
    Obtiene las tareas de una lista con filtros opcionales y calcula el porcentaje de completitud.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista cuyas tareas se consultan.
        is_done (Optional[bool]): Filtrar tareas completadas o no.
        priority (Optional[str]): Filtrar tareas por nivel de prioridad.

    Returns:
        Tuple[List[TaskModel], float]: Lista filtrada de tareas y porcentaje de tareas completadas.

    Raises:
        HTTPException 500: Si ocurre un error inesperado durante la consulta.
    """
    try:
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
    except Exception as e:
        logger.error(f"Error fetching tasks for list {list_id} with filters: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tasks")