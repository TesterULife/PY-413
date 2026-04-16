import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.engine import Base


class Profile(Base):
    __tablename__ = 'profiles'
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(nullable=False, default='offline')
    birthday: Mapped[datetime.date] = mapped_column(nullable=False)
    bio: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[int] = mapped_column(nullable=False)
    joined_at: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'),
        unique=True
    )

    user: Mapped['User'] = relationship(back_populates='profiles')
