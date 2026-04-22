import logging
from pathlib import Path

from sqlalchemy import select, UUID

from src.engine import sync_session_factory
from src.models.admin import AdminLog
from src.models.role import Role
from src.models.userrole import UserRole
from src.security.decorators import requires_roles

"""
4. CRUD для ролей
Создайте набор операций:

create_role(name, description) — добавить новую роль.
get_roles() — получить список всех ролей.
update_role(role_id, **fields) — изменить название или описание.
delete_role(role_id) — удалить роль (только если нет пользователей с этой ролью).
"""

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

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
def create_role(admin_id: UUID, name: str, description: str):
    with sync_session_factory() as session:
        with session.begin():
            role = Role(
                name_role=name,
                description=description
            )

            log = AdminLog(
                admin_id=admin_id,
                target_user_id=None,
                operation='create_role'
            )

            session.add(log)
            session.add(role)

            return role


def get_roles():
    with sync_session_factory() as session:
        query = select(Role)
        result = session.execute(query)

        return result.scalars().all()


@requires_roles('admin')
def update_role(admin_id: UUID, role_id: int, **fields):
    with sync_session_factory() as session:
        with session.begin():
            role = session.query(Role).filter_by(id=role_id).first()

            if not role:
                raise ValueError('Role not found')

            for key, value in fields.items():
                if hasattr(role, key):
                    setattr(role, key, value)
                else:
                    raise ValueError(f'Field {key} does not exist')

            log = AdminLog(
                admin_id=admin_id,
                target_user_id=None,
                operation='update_role'
            )
            session.add(log)

            return role


@requires_roles('admin')
def delete_role(admin_id: UUID, role_id: int):
    with sync_session_factory() as session:
        with session.begin():
            role = session.query(Role).filter_by(id=role_id).first()

            if not role:
                raise ValueError("Role not found")

            exists = session.query(UserRole).filter_by(role_id=role_id).first()

            if exists:
                raise ValueError("Can not delete role with assigned users")

            log = AdminLog(
                admin_id=admin_id,
                target_user_id=None,
                operation='delete_role'
            )

            session.add(log)
            session.delete(role)
