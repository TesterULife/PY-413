import datetime

from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

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


class Profile(Base):
    __tablename__ = 'profiles'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(nullable=False, default='offline')
    birthday: Mapped[datetime.date] = mapped_column(nullable=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[int] = mapped_column(nullable=True)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id'),
        primary_key=True
    )

    user: Mapped['User'] = relationship(back_populates='profile')
