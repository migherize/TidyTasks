"""
Endpoints para gestión de tareas dentro de listas.

Incluye creación, consulta, actualización, eliminación
y cambio de estado de tareas en listas específicas.
"""

import logging

from fastapi import APIRouter, Body, Depends, Path, status, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.api.schemas.task import (
    StatusChangeRequest,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.domain.models.exceptions import TaskNotFoundException
from app.core.auth.dependencies import get_current_user
from app.infrastructure.db.crud.task import (
    create_task,
    delete_task,
    get_task,
    update_task,
    update_task_status,
)
from app.infrastructure.db.models.user import UserModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lists/{list_id}/tasks", tags=["Tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva tarea",
)
def create_task_endpoint(
    list_id: int = Path(
        ..., gt=0, description="ID de la lista a la que pertenece la tarea"
    ),
    task: TaskCreate = Body(..., description="Datos de la nueva tarea"),
    db: Session = Depends(deps.get_db_session),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    """
    Crear una nueva tarea en una lista específica.

    Este endpoint permite al usuario autenticado crear una tarea dentro de una lista
    identificada por su `list_id`. La tarea será registrada con el usuario como creador.

    ## Validaciones
    - **Título**: debe tener entre 3 y 200 caracteres.
    - **Descripción**: opcional, máximo 1000 caracteres.
    - **Prioridad**: uno de los siguientes valores válidos:
      - `"high"`
      - `"medium"`
      - `"low"`

    ## Requiere Autenticación
    El token JWT debe ser enviado usando el esquema `Bearer` en el encabezado `Authorization`.

    ## Parámetros de ruta
    - **list_id** (int): ID de la lista a la que se asignará la nueva tarea.

    ## Cuerpo de la solicitud
    - **title** (str): Título de la tarea.
    - **description** (str, opcional): Detalle adicional de la tarea.
    - **priority** (str): Prioridad de la tarea (alta, media o baja).

    ## Ejemplo de solicitud
    ```json
    {
        "title": "Comprar pan",
        "description": "Ir a la panadería antes de las 8 PM",
        "priority": "medium"
    }
    ```

    ## Respuesta
    Retorna un objeto con los detalles de la tarea recién creada.
    """

    logger.info("Creating task in list %d: %s", list_id, task.dict())
    try:
        return create_task(db, list_id, task, created_by_id=current_user.id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Unexpected error creating task: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.get("/{task_id}", response_model=TaskResponse, summary="Obtener una tarea")
def get_task_endpoint(
    list_id: int = Path(..., gt=0),
    task_id: int = Path(..., gt=0),
    db: Session = Depends(deps.get_db_session),
    current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    """
    Obtiene una tarea por su ID y el ID de su lista.
    """
    logger.info("Fetching task %d from list %d", task_id, list_id)
    task = get_task(db, list_id, task_id)
    if not task:
        raise TaskNotFoundException(task_id)

    if task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return task


@router.put("/{task_id}", response_model=TaskResponse, summary="Actualizar una tarea")
def update_task_endpoint(
    list_id: int = Path(..., gt=0),
    task_id: int = Path(..., gt=0),
    task: TaskUpdate = Body(...),
    db: Session = Depends(deps.get_db_session),
    _current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    """
    Actualiza una tarea existente dentro de una lista.

    Se pueden enviar campos parciales para actualizar solo ciertos valores.
    Por Ejemplo, solo `title` o `is_done`.
    ### Campos actualizables:
    - `title`: título de la tarea.
    - `description`: descripción opcional.
    - `priority`: nivel de prioridad (`low`, `medium`, `high`, etc.).
    - `is_done`: marcar como completada o no.
    - `assigned_to`: id del usuario asignado (puede ser `null` para desasignar).

    ### Campos **no actualizables** desde este endpoint:
    - `id`: ID de la tarea.
    - `list_id`: ID de la lista (no se permite mover la tarea a otra lista).
    - `created_by`: usuario creador (lo determina el sistema).
    - `created_at`: fecha de creación (autogenerada).
    - `updated_at`: fecha de modificación (autogenerada).

    Retorna la tarea actualizada o un error si no se encuentra.
    """
    logger.info(
        "Updating task %d in list %d with data: %s",
        task_id,
        list_id,
        task.dict(exclude_unset=True),
    )
    updated_task = update_task(db, list_id, task_id, task)
    if not updated_task:
        raise TaskNotFoundException(task_id)

    return updated_task


@router.delete(
    "/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una tarea"
)
def delete_task_endpoint(
    list_id: int = Path(..., gt=0),
    task_id: int = Path(..., gt=0),
    db: Session = Depends(deps.get_db_session),
    _current_user: UserModel = Depends(get_current_user),
):
    """
    Elimina una tarea específica por ID dentro de una lista.
    """
    logger.info("Deleting task %d from list %d", task_id, list_id)
    deleted = delete_task(db, list_id, task_id)
    if not deleted:
        raise TaskNotFoundException(task_id)


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse,
    summary="Cambiar estado de una tarea",
)
def change_task_status(
    list_id: int = Path(..., gt=0),
    task_id: int = Path(..., gt=0),
    status_request: StatusChangeRequest = Body(...),
    db: Session = Depends(deps.get_db_session),
    _current_user: UserModel = Depends(get_current_user),
) -> TaskResponse:
    """
    Cambia el estado de completitud (`is_done`) de una tarea específica.
    """
    logger.info(
        "Changing status of task %d in list %d to: %s",
        task_id,
        list_id,
        status_request.is_done,
    )
    task = update_task_status(db, list_id, task_id, status_request.is_done)
    if not task:
        raise TaskNotFoundException(task_id)
    return task
