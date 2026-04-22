import uuid

import pytest

from src.engine import sync_session_factory
from src.models.group import Group
from src.security.decorators import Forbidden
from src.services.crud_group import (
    create_group,
    get_group,
    update_group,
    delete_group,
    add_user_in_group,
    remove_user_from_group
)
from src.services.user_service import register_user


def test_create_group(admin):
    title = f'{uuid.uuid4()} group'

    group = create_group(
        admin_id=admin,
        title=title,
    )

    assert group is not None
    assert group.title == title


def test_get_group(simple_group):
    groups = get_group()

    assert isinstance(groups, list)
    assert any(g.id == simple_group.id for g in groups)


def test_update_group(admin, simple_group):
    new_title = f'{uuid.uuid4()} group'

    updated = update_group(
        admin_id=admin,
        group_id=simple_group.id,
        title=new_title

    )

    assert updated is not None
    assert updated.id == simple_group.id
    assert updated.title == new_title


def test_delete_group(admin, simple_group):
    group_id = simple_group.id

    delete_group(
        admin_id=admin,
        group_id=group_id,
    )

    with sync_session_factory() as session:
        group = session.query(Group).filter_by(id=group_id).first()

        assert group is None


def test_add_user_in_group(admin, simple_group, uniq_email):
    user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='Testing User'
    )

    target_group = simple_group

    add_user_in_group(
        admin_id=admin,
        user_id=user.id,
        group_id=target_group.id,
    )

    with sync_session_factory() as session:
        group = session.get(Group, simple_group.id)

        users_ids = [u.id for u in group.users]

        assert user.id in users_ids


def test_remove_user_from_group(admin, simple_group, uniq_email):
    user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='Testing User',
    )

    add_user_in_group(
        admin_id=admin,
        user_id=user.id,
        group_id=simple_group.id,
    )

    with sync_session_factory() as session:
        group = session.get(Group, simple_group.id)
        session.refresh(group)

        users_ids = [u.id for u in group.users]
        assert user.id in users_ids

    remove_user_from_group(
        admin_id=admin,
        user_id=user.id,
        group_id=simple_group.id,
    )

    with sync_session_factory() as session:
        group = session.get(Group, simple_group.id)
        session.refresh(group)

        users_ids = [u.id for u in group.users]
        assert user.id not in users_ids


def test_add_user_with_wrong_role(simple_group, uniq_email):
    simple_user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='I am want to be a manager'
    )

    target_user = register_user(
        email=uniq_email(),
        password='PassWord',
        full_name='Give me Access'
    )

    target_group = simple_group

    with pytest.raises(Forbidden):
        add_user_in_group(
            admin_id=simple_user.id,
            user_id=target_user.id,
            group_id=target_group.id,
        )
