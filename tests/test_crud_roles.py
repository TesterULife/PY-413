import pytest

from src.services.crud_roles import create_role, get_roles, update_role, delete_role
from src.services.role_service import assign_role


def test_create_role(admin):
    role = create_role(
        admin_id=admin,
        name='manager',
        description='manager can add users but can not delete them'
    )

    assert role is not None
    assert role.name_role == 'manager'


def test_get_roles(admin):
    roles = get_roles()

    assert roles is not None
    assert isinstance(roles, list)


def test_update_role(admin):
    roles = get_roles()
    role = roles[0]

    update_role(
        admin_id=admin,
        role_id=role.id,
        name_role='new_role',
        description='I little bit changed this role'
    )

    updated_role = next(r for r in get_roles() if r.id == role.id)

    assert updated_role.name_role == 'new_role'
    assert updated_role.description == 'I little bit changed this role'


def test_success_delete_role(admin):
    role = create_role(
        admin_id=admin,
        name='half user',
        description='This is tests role'

    )

    test_deleted = role.id

    delete_role(
        admin_id=admin,
        role_id=test_deleted
    )

    roles = get_roles()

    assert all(r.id != test_deleted for r in roles)


def test_delete_role_with_users_forbidden(admin, uniq_role):
    assign_role(
        admin_id=admin,
        user_id=admin,
        role_name=uniq_role.name_role
    )

    with pytest.raises(ValueError):
        delete_role(
            admin_id=admin,
            role_id=uniq_role.id
        )
