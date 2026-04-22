from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,  # all request
    # pool_size = 5, # подключения
    # max_overflow = 10 # дополнительные подключения
)

sync_session_factory = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
