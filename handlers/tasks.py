from fastapi import APIRouter, Depends
from typing import Annotated
from schemas import TaskSchema, TaskCreateSchema
from repository import TaskRepository
from dependency import get_task_service, get_task_repository, get_request_user_id
from service import TaskService

task_router = APIRouter(prefix='/task', tags=['task'])


@task_router.get('/all', response_model=list[TaskSchema])
async def get_tasks(
        task_service: Annotated[TaskService, Depends(get_task_service)],
):
    return task_service.get_tasks()


@task_router.post('/', response_model=TaskSchema)
async def create_task(
        body: TaskCreateSchema,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    task = task_service.create_task(body, user_id)
    return task


@task_router.put('/{task_id}')
async def update_task(
        task_id: int,
        name: str,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    return task_service.update_task_name(task_id, name, user_id)


@task_router.patch('/{task_id}', response_model=TaskSchema)
async def patch_task(
        task_id: int,
        name: str,
        task_service: Annotated[TaskService, Depends(get_task_service)],
        user_id: int = Depends(get_request_user_id)
):
    return task_service.update_task_name(task_id, name, user_id)


@task_router.delete('/{task_id}')
async def delete_task(
        task_id: int,
        task_repository: Annotated[TaskRepository, Depends(get_task_repository)]
):
   task_repository.delete_task(task_id)
   return {'message': 'task is deleted'}
