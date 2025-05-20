from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlite_db_name: str = 'pomodoro.sqlite'
    redis_password: str = 'eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81'
