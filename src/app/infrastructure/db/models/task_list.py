from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.infrastructure.db.base import Base

class TaskListModel(Base):
    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color_tag = Column(String, nullable=True)
    category = Column(String, nullable=True)

    tasks = relationship("TaskModel", back_populates="task_list")
