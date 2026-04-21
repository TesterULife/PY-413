import datetime

from sqlalchemy import text, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.engine import Base

"""
7. Логирование действий админа

Создайте модель AdminLog (админ, действие, время, целевой пользователь). 
Вставляйте запись в AdminLog при каждом изменении ролей 
или удалении пользователей администратором.
"""


class AdminLog(Base):
    __tablename__ = 'admin_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    operation: Mapped[str] = mapped_column(nullable=False)
    time_operation: Mapped[datetime.datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    admin_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    target_user_id: Mapped[UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True,
    )

    admin: Mapped['User'] = relationship(
        foreign_keys=[admin_id],
        backref='admin_actions'
    )

    target_user: Mapped['User'] = relationship(
        foreign_keys=[target_user_id],
        backref='target_actions'
    )
