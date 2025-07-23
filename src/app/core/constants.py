from enum import Enum

class TaskListError(str, Enum):
    CREATION_FAILED = "Task list creation failed"

class PriorityLevel(str, Enum):
    """
    Niveles permitidos de prioridad para una tarea.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"