from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.engine import Base

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


class UserRole(Base):
    __tablename__ = 'users_role'
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.id', ondelete='CASCADE'),
        primary_key=True
    )
