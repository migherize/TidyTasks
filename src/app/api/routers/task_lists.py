from fastapi import APIRouter, Depends, status, Query, Path
from sqlalchemy.orm import Session
from typing import Optional
from app.api import deps
from app.core.constants import PriorityLevel
from app.api.schemas.task_list import TaskListWithCompletionResponse, TaskListRequest, TaskListResponse
from app.infrastructure.db.crud.task_list import (
    create_task_list,
    get_task_list,
    update_task_list,
    delete_task_list,
    get_tasks_with_filters
)

router = APIRouter(prefix="/lists", tags=["Task Lists"])

@router.post(
    "/",
    response_model=TaskListResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva lista de tareas",
    response_description="La lista de tareas creada exitosamente"
)
def create_list(list_data: TaskListRequest, db: Session = Depends(deps.get_db_session)) -> TaskListResponse:
    """
    Crea una nueva lista de tareas para organizar tus actividades.

    ## Ejemplo de cuerpo (JSON):
    ```json
    {
        "name": "Mi lista semanal"
    }
    ```

    - El campo `name` debe ser único y contener entre 3 y 50 caracteres alfanuméricos.
    - Se devolverá la lista creada junto con sus tareas asociadas (vacía por defecto).

    ### Respuestas:
    - ✅ **201**: Lista creada exitosamente.
    - ❌ **400**: Datos inválidos en la solicitud.
    - ❌ **500**: Error interno al crear la lista.

    """
    return create_task_list(db, list_data)

@router.get("/{list_id}", response_model=TaskListResponse, summary="Obtener una lista de tareas")
def get_list(
    list_id: int = Path(..., gt=0, description="ID de la lista de tareas"),
    db: Session = Depends(deps.get_db_session)
) -> TaskListResponse:
    """
    Obtiene una lista de tareas por su ID.

    - Si no existe, retorna un error 404.
    """
    return get_task_list(db, list_id)


@router.put("/{list_id}", response_model=TaskListResponse, summary="Actualizar una lista de tareas")
def update_list(
    list_id: int = Path(..., gt=0, description="ID de la lista de tareas a actualizar"),
    list_data: TaskListRequest = ...,
    db: Session = Depends(deps.get_db_session)
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


@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar una lista de tareas")
def delete_list(
    list_id: int = Path(..., gt=0, description="ID de la lista de tareas a eliminar"),
    db: Session = Depends(deps.get_db_session)
):
    """
    Elimina una lista de tareas por su ID.

    - No retorna contenido si es exitosa.
    """
    delete_task_list(db, list_id)


@router.get("/", response_model=TaskListWithCompletionResponse, summary="Listar tareas de una lista")
def list_tasks(
    list_id: int = Query(..., gt=0, description="ID de la lista de tareas"),
    is_done: Optional[bool] = Query(None, description="Filtrar por tareas completadas"),
    priority: Optional[PriorityLevel] = Query(None, description="Filtrar por prioridad (ej: alta, media, baja)"),
    db: Session = Depends(deps.get_db_session)
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
    return {
        "tasks": tasks,
        "completion_percentage": percentage
    }