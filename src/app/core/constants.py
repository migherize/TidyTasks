"""
Definición de enumerados usados en TidyTasks para errores y niveles de prioridad.
"""

from enum import Enum


class TaskListError(str, Enum):
    """
    Errores relacionados con la creación y manejo de listas de tareas.
    """

    CREATION_FAILED = "Task list creation failed"


class PriorityLevel(str, Enum):
    """
    Niveles permitidos de prioridad para una tarea.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ColorTagEnum(str, Enum):
    """
    Colores permitidos de list de tareas.
    """

    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    PURPLE = "purple"
    ORANGE = "orange"
