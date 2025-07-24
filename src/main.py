"""
Módulo principal de la aplicación TidyTasks.
Define la configuración de logging, inicializa la base de datos
y crea la instancia de FastAPI con las rutas incluidas.
"""

import logging
from pathlib import Path
from fastapi import FastAPI
from app.api.routers.task_lists import router as api_router_task_lists
from app.api.routers.tasks import router as api_router_tasks
from app.api.routers.auth import router as api_router_auth
from app.infrastructure.db.base import Base
from app.infrastructure.db.session import engine

log_path = Path("logs/app.log")
log_path.parent.mkdir(parents=True, exist_ok=True)

if not log_path.exists():
    log_path.touch()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler(log_path), logging.StreamHandler()],
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def home_page():
    """
    Clasica pagina de inicio de Fastapi
    """
    return {"page": "home", "Version": "1.0", "Update Date": "Jul 23 2025"}


app.include_router(api_router_auth)
app.include_router(api_router_task_lists)
app.include_router(api_router_tasks)
