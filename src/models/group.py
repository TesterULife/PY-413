import datetime

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.engine import Base

"""
9. Группы пользователей
Модель Group и связующая UserGroup.

Операции CRUD для групп.
Привязка/отвязка пользователей к группам.
Ограничение: в группе «Managers» могут быть только пользователи 
с ролью «manager» или «admin».
"""


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    users: Mapped[list['User']] = relationship(
        secondary='user_group',
        back_populates='groups'
    )
