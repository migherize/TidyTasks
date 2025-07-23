"""
Módulo de operaciones CRUD para la gestión de listas de tareas y tareas asociadas.

Este módulo contiene funciones para crear, obtener, actualizar y eliminar listas de tareas, así
como para consultar tareas con filtros específicos y calcular el porcentaje de tareas completadas.

Utiliza SQLAlchemy para la interacción con la DB y FastAPI HTTPException para manejo de errores.

Funciones principales:
- create_task_list: Crea una nueva lista de tareas.
- get_task_list: Obtiene una lista de tareas por ID.
- update_task_list: Actualiza una lista de tareas existente.
- delete_task_list: Elimina una lista de tareas por ID.
- get_tasks_with_filters: Obtiene tareas filtradas y calcula porcentaje de completitud.

Cada función registra logs de operaciones y errores para facilitar el monitoreo y debugging.
"""

import logging
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.constants import TaskListError
from app.domain.models.exceptions import TaskListCreationException
from app.domain.models.task_list import TaskListCreate
from app.infrastructure.db.models.task import TaskModel
from app.infrastructure.db.models.task_list import TaskListModel

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
        logger.info("Creating task list: %s", list_data.dict())
        db_list = TaskListModel(**list_data.dict())
        db.add(db_list)
        db.commit()
        db.refresh(db_list)
        return db_list
    except Exception as e:
        logger.error("Error creating task list: %s", e)
        raise TaskListCreationException(detail=TaskListError.CREATION_FAILED) from e


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
        logger.info("Getting task list ID: %s", list_id)
        db_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
        if not db_list:
            logger.warning("Task list %s not found", list_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
            )
        return db_list
    except Exception as e:
        logger.error("Error getting task list %s: %s", list_id, e)
        raise HTTPException(status_code=500, detail="Failed to get task list") from e


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
        logger.info("Updating task list ID %s with: %s", list_id, list_data.dict())
        db_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
        if not db_list:
            logger.warning("Task list %s not found for update", list_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
            )
        for key, value in list_data.dict().items():
            setattr(db_list, key, value)
        db.commit()
        db.refresh(db_list)
        return db_list
    except Exception as e:
        logger.error("Error updating task in list %s: %s", list_id, e)
        raise HTTPException(status_code=500, detail="Failed to update task list") from e


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
        logger.info("Deleting task list ID: %s", list_id)
        db_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
        if not db_list:
            logger.warning("Task list %s not found for deletion", list_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="List not found"
            )
        db.delete(db_list)
        db.commit()
    except Exception as e:
        logger.error("Error deleting task list %s: %s", list_id, e)
        raise HTTPException(status_code=500, detail="Failed to delete task list") from e


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
        logger.error("Error fetching tasks for list %s with filters: %s", list_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch tasks") from e
