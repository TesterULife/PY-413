import pytest

from src.engine import sync_session_factory
from src.models.user import User
from src.services.crud_roles import create_role
from src.services.role_service import assign_role, remove_role
from src.services.user_service import register_user


def test_assign_role(admin, uniq_email):
    user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='Testing User'
    )

    create_role(
        admin_id=admin,
        name='manager',
        description='test role'
    )

    assign_role(
        admin_id=admin,
        user_id=user.id,
        role_name='manager'
    )

    with sync_session_factory() as session:
        user_db = session.query(User).filter_by(id=user.id).first()
        role_names = [r.name_role for r in user_db.roles]

        assert 'manager' in role_names


def test_assign_duplicate_role(admin, uniq_email):
    user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='Testing User'
    )

    create_role(
        admin_id=admin,
        name='manager',
        description='test role'
    )

    assign_role(
        admin_id=admin,
        user_id=user.id,
        role_name='manager'
    )

    with pytest.raises(ValueError):
        assign_role(
            admin_id=admin,
            user_id=user.id,
            role_name='manager'
        )


def test_remove_role(admin, uniq_email):
    user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='Testing User'
    )

    create_role(
        admin_id=admin,
        name='Role for delete',
        description='Empty'
    )

    assign_role(
        admin_id=admin,
        user_id=user.id,
        role_name='Role for delete'
    )

    remove_role(
        admin_id=admin,
        user_id=user.id,
        role_name='Role for delete',
    )

    with sync_session_factory() as session:
        user_db = session.query(User).filter_by(id=user.id).first()
        role_names = [r.name_role for r in user_db.roles]

        assert 'Role for delete' not in role_names


def test_remove_last_role(admin, uniq_email):
    user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='Testing User'
    )

    create_role(
        admin_id=admin,
        name='manager',
        description='test role'
    )

    assign_role(
        admin_id=admin,
        user_id=user.id,
        role_name='manager'
    )

    remove_role(
        admin_id=admin,
        user_id=user.id,
        role_name='manager'
    )

    with pytest.raises(ValueError):
        remove_role(
            admin_id=admin,
            user_id=user.id,
            role_name='user'
        )
