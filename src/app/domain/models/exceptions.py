"""
Excepciones personalizadas para la gestión de listas de tareas y tareas.
"""

from fastapi import HTTPException, status


class TaskListCreationException(HTTPException):
    """
    Excepción lanzada cuando no se puede crear una lista de tareas.
    """

    def __init__(self, detail: str = "Task list could not be created"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class TaskListNotFoundException(HTTPException):
    """
    Excepción lanzada cuando no se encuentra una lista de tareas por su ID.
    """

    def __init__(self, list_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La lista de tareas con ID {list_id} no fue encontrada",
        )


class TaskNotFoundException(HTTPException):
    """
    Excepción lanzada cuando no se encuentra una tarea por su ID.
    """

    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarea con ID {task_id} no encontrada",
        )
