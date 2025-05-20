from handlers.tasks import task_router
from handlers.ping import ping_router

routers = [
    task_router,
    ping_router,
]
