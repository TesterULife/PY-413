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


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_role: Mapped[str] = mapped_column(nullable=False, default='user')
    description: Mapped[str] = mapped_column(nullable=True)

    roles: Mapped[list['User']] = relationship(
        secondary='user_roles',
        back_populates='roles'
    )
