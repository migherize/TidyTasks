"""
CRUD para operaciones sobre el modelo TaskModel: creación, consulta,
actualización, eliminación y cambio de estado de tareas.
"""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.domain.models.task import TaskCreate, TaskUpdate
from app.infrastructure.db.models.task import TaskModel
from app.infrastructure.db.models.task_list import TaskListModel
from app.infrastructure.db.models.user import UserModel
from app.infrastructure.email.notifier import notify_assigned_user

logger = logging.getLogger(__name__)


def create_task(
    db: Session, list_id: int, task_data: TaskCreate, created_by_id: int
) -> TaskModel:
    """
    Crea una nueva tarea asociada a una lista específica.

    Args:
        db (Session): Sesión activa de base de datos.
        list_id (int): ID de la lista a la que se asignará la tarea.
        task_data (TaskCreate): Datos de la tarea a crear.

    Returns:
        TaskModel: Instancia de la tarea creada.

    Raises:
        HTTPException 404: Si la lista o usuario asignado no existen.
        HTTPException 400: Si hay error de integridad.
        HTTPException 500: Otros errores inesperados.
    """
    try:
        task_list = db.query(TaskListModel).filter(TaskListModel.id == list_id).first()
        if not task_list:
            raise HTTPException(status_code=404, detail="Task list not found")

        assigned_id = task_data.assigned_to
        if assigned_id == 0:
            assigned_id = None

        assignee = None
        if task_data.assigned_to:
            assignee = (
                db.query(UserModel)
                .filter(UserModel.id == task_data.assigned_to)
                .first()
            )
            if not assignee:
                raise HTTPException(
                    status_code=404, detail="Usuario asignado no existe"
                )

        task_dict = task_data.dict()
        if task_dict["assigned_to"] == 0:
            task_dict["assigned_to"] = None

        logger.info("Creating task in list %d: %s", list_id, task_dict)
        db_task = TaskModel(**task_dict, list_id=list_id, created_by=created_by_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        if assignee:
            logger.info(
                "[NOTIFICACIÓN FICTICIA] Se notificó al usuario %s (%s) sobre la tarea '%s'.",
                assignee.username,
                assignee.email,
                db_task.title,
            )
            notify_assigned_user(assignee.email, db_task.title)

        return db_task

    except IntegrityError as e:
        logger.warning("Integrity error creating task: %s", e.orig)
        raise HTTPException(
            status_code=400,
            detail="Database integrity error: possible duplicate or invalid data",
        ) from e
    except HTTPException:
        raise  # Propaga HTTPExceptions ya lanzadas arriba
    except Exception as e:
        logger.error("Unexpected error creating task: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to create task") from e


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
        logger.error("Error fetching task %d from list %d: %s", task_id, list_id, e)
        raise HTTPException(status_code=500, detail="Failed to fetch task") from e


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
            "Updating task %d in list %d with data: %s",
            task_id,
            list_id,
            task_data.dict(exclude_unset=True),
        )

        updated_data = task_data.dict(exclude_unset=True)

        if "assigned_to" in updated_data and updated_data["assigned_to"] == 0:
            updated_data["assigned_to"] = None

        for key, value in updated_data.items():
            setattr(db_task, key, value)

        for key, value in updated_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
        return db_task
    except Exception as e:
        logger.error(
            "Error updating task %d in list %d: %s",
            task_id,
            list_id,
            e,
        )
        raise HTTPException(status_code=500, detail="Failed to update task") from e


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
            return False
        logger.info("Deleting task %s from list %s", task_id, list_id)
        db.delete(db_task)
        db.commit()
        return True
    except Exception as e:
        logger.error("Error deleting task %s from list %s: %s", task_id, list_id, e)
        raise HTTPException(status_code=500, detail="Failed to delete task") from e


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

        logger.info(
            "Updating status of task %s in list %s to %s", task_id, list_id, is_done
        )
        task.is_done = is_done
        db.commit()
        db.refresh(task)
        return task
    except Exception as e:
        logger.error(
            "Error updating status for task %s in list %s: %s", task_id, list_id, e
        )
        raise HTTPException(
            status_code=500, detail="Failed to update task status"
        ) from e
