from fastapi import HTTPException, status

class TaskListCreationException(HTTPException):
    def __init__(self, detail: str = "Task list could not be created"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class TaskListCreationException(HTTPException):
    def __init__(self, detail: str = "No se pudo crear la lista de tareas"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class TaskListNotFoundException(HTTPException):
    def __init__(self, list_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La lista de tareas con ID {list_id} no fue encontrada"
        )