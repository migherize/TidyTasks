from fastapi import FastAPI
from app.api.routers.tasks import router as api_router_tasks
from app.api.routers.task_lists import router as api_router_task_lists

app = FastAPI()
app.include_router(api_router_tasks)
app.include_router(api_router_task_lists)
