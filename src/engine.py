import datetime

from sqlalchemy import create_engine, text, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column
from sqlalchemy.sql.annotation import Annotated

from src.config import settings

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,  # all request
    # pool_size = 5, # подключения
    # max_overflow = 10 # дополнительные подключения
)

sync_session_factory = sessionmaker(sync_engine)


# intpk = Annotated[int, mapped_column(primary_key=True)]
# created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
# str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    # type_annotation_map = {
    #     str_256: String(256)
    # }
    pass
