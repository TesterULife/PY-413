import datetime
import uuid

from sqlalchemy import text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.engine import Base
import src.models.userrole
import src.models.usergroup
from src.models.group import Group
from src.models.profile import Profile
from src.models.admin import AdminLog

"""
1. Модели и миграции
Создайте модели SQLAlchemy для сущностей: 
User, 
Role, 
UserRole (связующая таблица), 
Profile (дополнительная информация о пользователе). 

Реализуйте миграции для создания этих таблиц 
с соблюдением целостности (FK, уникальные и не-null поля).
"""

class User(Base):
    __tablename__ = 'users'
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"))

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)

    joined_at: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    # Flag from hw - task 8
    is_deleted: Mapped[bool] = mapped_column(
        nullable=False,
        default=False
    )

    profile: Mapped['Profile'] = relationship(
        back_populates='user',
        uselist=False
    )
    roles: Mapped[list['Role']] = relationship(
        secondary='user_roles',
        back_populates='roles'
    )

    groups: Mapped[list['Group']] = relationship(
        secondary='user_groups',
        back_populates='users'
    )