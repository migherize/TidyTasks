"""
Rutas (endpoints) para gestión de listas de tareas (Task Lists).

Incluye creación, consulta, actualización, eliminación y listado
de tareas con filtros de completitud y prioridad.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.api import deps
from app.api.schemas.task_list import (
    TaskListRequest,
    TaskListResponse,
    TaskListWithCompletionResponse,
)
from app.core.auth.dependencies import get_current_user
from app.core.constants import PriorityLevel
from app.infrastructure.db.models.user import UserModel

from app.infrastructure.db.crud.task_list import (
    create_task_list,
    delete_task_list,
    get_task_list,
    get_tasks_with_filters,
    update_task_list,
)

router = APIRouter(prefix="/lists", tags=["Task Lists"])


@router.post(
    "/",
    response_model=TaskListResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva lista de tareas",
    response_description="La lista de tareas creada exitosamente",
)
def create_list(
    list_data: TaskListRequest,
    db: Session = Depends(deps.get_db_session),
    _current_user: UserModel = Depends(get_current_user),
) -> TaskListResponse:
    """
    Crea una nueva lista de tareas para organizar tus actividades.

    ## Ejemplo de cuerpo (JSON):
    ```json
    {
        "name": "Mi lista semanal",
        "color_tag": "red",
        "category": "trabajo"
    }
    ```

    - El campo `name` debe ser único y contener entre 3 y 50 caracteres alfanuméricos.
    - El campo `color_tag` es opcional y permite asociar un color a la lista.
        - Puede ser uno de los colores predefinidos como `"red"`, `"blue"`, `"green"`, etc.
    - El campo `category` también es opcional y puede ser usado para clasificar listas.

    ### Respuestas:
    - ✅ **201**: Lista creada exitosamente.
    - ❌ **400**: Datos inválidos en la solicitud.
    - ❌ **500**: Error interno al crear la lista.
    """
    return create_task_list(db, list_data)


@router.get(
    "/{list_id}", response_model=TaskListResponse, summary="Obtener una lista de tareas"
)
def get_list(
    list_id: int = Path(..., gt=0, description="ID de la lista de tareas"),
    db: Session = Depends(deps.get_db_session),
    _current_user: UserModel = Depends(get_current_user),
) -> TaskListResponse:
    """
    Obtiene una lista de tareas por su ID.

    - Si no existe, retorna un error 404.
    """
    return get_task_list(db, list_id)


@router.put(
    "/{list_id}",
    response_model=TaskListResponse,
    summary="Actualizar una lista de tareas",
)
def update_list(
    list_id: int = Path(..., gt=0, description="ID de la lista de tareas a actualizar"),
    list_data: TaskListRequest = ...,
    db: Session = Depends(deps.get_db_session),
    _current_user: UserModel = Depends(get_current_user),
) -> TaskListResponse:
    """
    Actualiza el nombre de una lista de tareas existente.

    ## Ejemplo:
    ```json
    {
      "name": "Lista actualizada"
    }
    ```
    """
    return update_task_list(db, list_id, list_data)


@router.delete(
    "/{list_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una lista de tareas",
)
def delete_list(
    list_id: int = Path(..., gt=0, description="ID de la lista de tareas a eliminar"),
    db: Session = Depends(deps.get_db_session),
    _current_user: UserModel = Depends(get_current_user),
):
    """
    Elimina una lista de tareas por su ID.

    - No retorna contenido si es exitosa.
    """
    delete_task_list(db, list_id)


@router.get(
    "/",
    response_model=TaskListWithCompletionResponse,
    summary="Listar tareas de una lista",
)
def list_tasks(
    list_id: int = Query(..., gt=0, description="ID de la lista de tareas"),
    is_done: Optional[bool] = Query(None, description="Filtrar por tareas completadas"),
    priority: Optional[PriorityLevel] = Query(
        None, description="Filtrar por prioridad (ej: alta, media, baja)"
    ),
    db: Session = Depends(deps.get_db_session),
    _current_user: UserModel = Depends(get_current_user),
) -> TaskListWithCompletionResponse:
    """
    Lista las tareas asociadas a una lista específica, con opción de filtros por estado y prioridad.

    También devuelve el porcentaje de completitud de la lista.

    ### Parámetros:
    - `is_done`: Filtra tareas completadas o no.
    - `priority`: Filtra por nivel de prioridad.

    ### Ejemplo de respuesta:
    ```json
    {
      "tasks": [...],
      "completion_percentage": 60.0
    }
    ```
    """
    tasks, percentage = get_tasks_with_filters(db, list_id, is_done, priority)
    return {"tasks": tasks, "completion_percentage": percentage}
