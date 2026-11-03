from fastapi import FastAPI
from src.utils.db import Base,engin
from src.task.router import task_router
from src.user.router import user_routes


Base.metadata.create_all(engin)


app = FastAPI(title="This is my task management API")
app.include_router(task_router)
app.include_router(user_routes)