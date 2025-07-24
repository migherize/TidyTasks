"""
Definición del modelo TaskModel para representar tareas individuales dentro de una
lista de tareas en la base de datos.
"""

# pylint: disable=not-callable, too-few-public-methods

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class TaskModel(Base):
    """
    Modelo que representa una tarea dentro de una lista de tareas.
    Cada tarea puede tener un usuario asignado (mediante UUID).
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    priority = Column(String(50), nullable=False)
    is_done = Column(Boolean, default=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)
    list_id = Column(Integer, ForeignKey("task_lists.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    task_list = relationship("TaskListModel", back_populates="tasks")
    creator = relationship(
        "UserModel", foreign_keys=[created_by], backref="created_tasks"
    )
    assignee = relationship("UserModel", foreign_keys=[assigned_to])
