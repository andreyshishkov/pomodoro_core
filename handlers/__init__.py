from handlers.tasks import task_router
from handlers.ping import ping_router
from handlers.user import router as user_router
from handlers.auth import router as auth_router

routers = [
    task_router,
    ping_router,
    user_router,
    auth_router,
]
