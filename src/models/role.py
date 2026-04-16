from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.engine import Base


class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name_role: Mapped[str] = mapped_column(nullable=False, default='user')

    roles: Mapped[list['User']] = relationship(
        secondary='user_roles',
        back_populates='roles'
    )
