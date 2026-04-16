import datetime
import uuid

from sqlalchemy import text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.engine import Base


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
    profile: Mapped['Profile'] = relationship(
        back_populates='user',
        uselist=False
    )
    roles: Mapped[list['Role']] = relationship(
        secondary='user_roles',
        back_populates='users'
    )
