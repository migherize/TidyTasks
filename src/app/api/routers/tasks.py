import logging
from fastapi import APIRouter, Depends, status, Path, Body
from sqlalchemy.orm import Session
from app.infrastructure.db.crud.task import (
    create_task, get_task, update_task,
    delete_task, update_task_status
)
from app.domain.models.exceptions import TaskNotFoundException
from app.api.schemas.task import TaskCreate, TaskUpdate, TaskResponse, StatusChangeRequest
from app.api import deps

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lists/{list_id}/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Crear una nueva tarea")
def create_task_endpoint(
    list_id: int = Path(..., gt=0, description="ID de la lista a la que pertenece la tarea"),
    task: TaskCreate = Body(..., description="Datos de la nueva tarea"),
    db: Session = Depends(deps.get_db_session)
) -> TaskResponse:
    """
    Crea una nueva tarea dentro de una lista de tareas.

    ### Ejemplo de cuerpo:
    ```json
    {
        "title": "Comprar pan",
        "description": "Ir a la panadería",
        "priority": "medium",
        "assigned_to": "123e4567-e89b-12d3-a456-426614174000"
    }
    ```
    """
    logger.info(f"Creating task in list {list_id}: {task.dict()}")
    return create_task(db, list_id, task)


@router.get("/{task_id}", response_model=TaskResponse, summary="Obtener una tarea")
def get_task_endpoint(
    list_id: int = Path(..., gt=0),
    task_id: int = Path(..., gt=0),
    db: Session = Depends(deps.get_db_session)
) -> TaskResponse:
    """
    Obtiene una tarea por su ID y el ID de su lista.
    """
    logger.info(f"Fetching task {task_id} from list {list_id}")
    task = get_task(db, list_id, task_id)
    if not task:
        raise TaskNotFoundException(task_id)
    return task


@router.put("/{task_id}", response_model=TaskResponse, summary="Actualizar una tarea")
def update_task_endpoint(
    list_id: int = Path(..., gt=0),
    task_id: int = Path(..., gt=0),
    task: TaskUpdate = Body(...),
    db: Session = Depends(deps.get_db_session)
) -> TaskResponse:
    """
    Actualiza una tarea existente dentro de una lista.

    Se pueden enviar campos parciales (por ejemplo, solo `is_done` o `title`).
    """
    logger.info(f"Updating task {task_id} in list {list_id} with data: {task.dict(exclude_unset=True)}")
    updated_task = update_task(db, list_id, task_id, task)
    if not updated_task:
        raise TaskNotFoundException(task_id)
    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una tarea")
def delete_task_endpoint(
    list_id: int = Path(..., gt=0),
    task_id: int = Path(..., gt=0),
    db: Session = Depends(deps.get_db_session)
):
    """
    Elimina una tarea específica por ID dentro de una lista.
    """
    logger.info(f"Deleting task {task_id} from list {list_id}")
    deleted = delete_task(db, list_id, task_id)
    if not deleted:
        raise TaskNotFoundException(task_id)


@router.patch("/{task_id}/status", response_model=TaskResponse, summary="Cambiar estado de una tarea")
def change_task_status(
    list_id: int = Path(..., gt=0),
    task_id: int = Path(..., gt=0),
    status: StatusChangeRequest = Body(...),
    db: Session = Depends(deps.get_db_session)
) -> TaskResponse:
    logger.info(f"Changing status of task {task_id} in list {list_id} to: {status.is_done}")
    task = update_task_status(db, list_id, task_id, status.is_done)
    if not task:
        raise TaskNotFoundException(task_id)
    return task
