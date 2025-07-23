from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, nullable=False)
    is_done = Column(Boolean, default=False)
    list_id = Column(Integer, ForeignKey("task_lists.id"))

    task_list = relationship("TaskList", back_populates="tasks")
