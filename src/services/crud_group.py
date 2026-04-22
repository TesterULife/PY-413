import logging
from pathlib import Path

from sqlalchemy import select, UUID

from src.engine import sync_session_factory
from src.models.group import Group
from src.models.user import User
from src.models.usergroup import UserGroup
from src.security.decorators import requires_roles

"""
9. Группы пользователей
Модель Group и связующая UserGroup.

Операции CRUD для групп.
Привязка/отвязка пользователей к группам.
Ограничение: в группе «Managers» могут быть только пользователи
с ролью «manager» или «admin».
"""

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True) # создай папку если её нет

LOG_FILE = LOG_DIR / "services.log"

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)


@requires_roles('admin')
def create_group(admin_id: UUID, title: str):
    if not title:
        raise ValueError("Title is required")

    with sync_session_factory() as session:
        exists = session.query(Group).filter_by(title=title).first()

        if exists:
            raise ValueError("Group already exists")

        group = Group(title=title)

        session.add(group)
        session.commit()
        session.refresh(group)

        return group


def get_group():
    with sync_session_factory() as session:
        query = select(Group)
        result = session.execute(query)
        return result.scalars().all()


@requires_roles('admin')
def update_group(admin_id: UUID, group_id: int, **fields):
    with sync_session_factory() as session:
        group = session.query(Group).filter_by(id=group_id).first()

        if not group:
            raise ValueError('Group not found')

        for key, value in fields.items():
            if hasattr(group, key):
                setattr(group, key, value)
            else:
                raise ValueError(f"Field '{key}' does not exist")

        session.commit()
        session.refresh(group)

        return group


@requires_roles('admin')
def delete_group(admin_id: UUID, group_id: int):
    with sync_session_factory() as session:
        group = session.query(Group).filter_by(id=group_id).first()

        if not group:
            raise ValueError('Group not found')

        exists = session.query(UserGroup).filter_by(group_id=group_id).first()

        if exists:
            raise ValueError("Cannot delete group with assigned users")

        session.delete(group)
        session.commit()


@requires_roles('admin')
def add_user_in_group(admin_id: UUID, user_id: UUID, group_id: int):
    with (sync_session_factory() as session):
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            raise ValueError('User not found')

        group = session.query(Group).filter_by(id=group_id).first()

        if not group:
            raise ValueError('Group not found')

        if group.title.lower() == 'managers':

            user_roles = [role.name_role.lower() for role in user.roles]

            if not any(r in ['admin', 'manager'] for r in user_roles):
                logger.warning(
                    "In Managers group allowed only admin or manager "
                    "(user_id=%s, roles=%s)",
                    user.id, user_roles
                )

                raise ValueError(
                    "In Managers group allowed only users "
                    "with role admin or manager"
                )

        exists = session.query(UserGroup).filter_by(
            user_id=user_id,
            group_id=group_id
        ).first()

        if exists:
            raise ValueError("User already in group")

        link = UserGroup(user_id=user_id, group_id=group_id)

        session.add(link)
        session.commit()
        session.refresh(link)

        return link


@requires_roles('admin')
def remove_user_from_group(admin_id: UUID, user_id: UUID, group_id: int):
    with sync_session_factory() as session:
        link = session.query(UserGroup).filter_by(
            user_id=user_id,
            group_id=group_id
        ).first()

        if not link:
            raise ValueError("User not in group")

        session.delete(link)
        session.commit()
