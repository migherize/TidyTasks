from fastapi import FastAPI
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine
from app.api.routers.tasks import router as api_router_tasks
from app.api.routers.task_lists import router as api_router_task_lists
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def home_page():
    """
    Clasica pagina de inicio de Fastapi
    """
    return {"page": "home", "Version": "1.0", "Update Date": "Jul 23 2025"}


app.include_router(api_router_tasks)
app.include_router(api_router_task_lists)
