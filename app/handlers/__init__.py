from app.handlers.tasks import task_router
from app.handlers.ping import ping_router
from app.handlers.user import router as user_router
from app.handlers.auth import router as auth_router

routers = [
    task_router,
    ping_router,
    user_router,
    auth_router,
]
