"""
Definición del modelo TaskListModel que representa una lista de tareas.
"""

# pylint: disable=too-few-public-methods

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class TaskListModel(Base):
    """
    Modelo que representa una lista de tareas.
    Puede tener múltiples tareas asociadas mediante la relación con TaskModel.
    """

    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    color_tag = Column(String(255), nullable=True)
    category = Column(String(255), nullable=True)

    tasks = relationship("TaskModel", back_populates="task_list")
