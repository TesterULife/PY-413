from sqlalchemy import UUID
import logging

from src.engine import sync_session_factory
from src.models.role import Role
from src.models.user import User
from src.models.userrole import UserRole
from src.models.admin import AdminLog
from src.security.decorators import requires_roles

"""
5. Назначение и снятие ролей
Напишите функции:

assign_role(user_id, role_name) 
— назначить роль пользователю (добавить в UserRole), если её ещё нет.

remove_role(user_id, role_name) 
— снять роль (удалить из [30.06.2025 14:13]UserRole), 
но нельзя снять последнюю роль у пользователя.
"""

logging.basicConfig(
    level=logging.INFO,
    filename='services.log',
    filemode='a',
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding='utf-8'
)

logger = logging.getLogger(__name__)


@requires_roles('admin')
def assign_role(admin_id: UUID, user_id: UUID, role_name: str):
    with sync_session_factory() as session:
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            raise ValueError('User not found')

        role = session.query(Role).filter_by(name_role=role_name).first()

        if not role:
            raise ValueError("Role not found")

        user_role = session.query(UserRole).filter_by(
            user_id=user_id,
            role_id=role.id
        ).first()

        if user_role:
            logger.warning(
                "User already has role (user_id=%s, role=%s)",
                user_id,
                role_name
            )
            raise ValueError('This user already have this role')

        new_user_role = UserRole(
            user_id=user_id,
            role_id=role.id
        )

        log = AdminLog(
            admin_id=admin_id,
            target_user_id=user_id,
            operation="assign_role"
        )

        session.add(log)

        session.add(new_user_role)
        session.commit()

        return True


@requires_roles('admin')
def remove_role(admin_id: UUID, user_id: UUID, role_name: str):
    with sync_session_factory() as session:
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            raise ValueError('User not found')

        role = session.query(Role).filter_by(name_role=role_name).first()

        if not role:
            raise ValueError('Role not found')

        user_role = session.query(UserRole).filter_by(
            user_id=user_id,
            role_id=role.id
        ).first()

        if not user_role:
            raise ValueError("This user doesn't have this role")

        user_roles = session.query(UserRole).filter_by(user_id=user_id).all()

        if len(user_roles) <= 1:
            logger.warning(
                "Attempt to remove last role (user_id=%s, role=%s)",
                user_id,
                role_name
            )
            raise ValueError("Can't remove last role")

        log = AdminLog(
            admin_id=admin_id,
            target_user_id=user_id,
            operation="remove_role"
        )

        session.add(log)

        session.delete(user_role)
        session.commit()

        return True
