from fastapi import APIRouter
from app.settings import Settings


ping_router = APIRouter(prefix='/ping', tags=['ping'])


@ping_router.get('/db')
async def ping_db():
    return {'message': 'ok'}


@ping_router.get('/app')
async def ping_app():
    return {'text': Settings().GOOGLE_TOKEN_ID}
