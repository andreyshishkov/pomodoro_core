from fastapi import FastAPI
from app.tasks.handlers import task_router
from app.users.user_profile.handlers import router as user_router
from app.users.auth.handlers import router as auth_router

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)

