from sqlalchemy import ForeignKey, UUID
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

class UserGroup(Base):
    __tablename__ = 'user_group'

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )

    group_id: Mapped[int] = mapped_column(
        ForeignKey('group.id', ondelete='CASCADE'),
        primary_key=True
    )
