from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from ..base import Base

class TaskList(Base):
    __tablename__ = "task_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color_tag = Column(String, nullable=True)
    category = Column(String, nullable=True)

    tasks = relationship("Task", back_populates="task_list")
