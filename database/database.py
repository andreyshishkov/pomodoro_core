from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql+psycopg2://user:password@localhost:5432/database')

Session = sessionmaker(engine)


def get_db_session() -> Session:
    return Session
