import pytest


from src.services.user_service import register_user
from src.services.role_service import assign_role
from src.queries.orm import (
    active_users_for_role,
    users_without_profile,
    group_by_registration_day
)

"""
8. Отчёты (запросы)

3–4 теста

активные пользователи по ролям
пользователи без профиля
группировка по датам

👉 тут просто проверка, что запрос не мусор
"""


def test_active_users_for_role(admin, uniq_email):
    user1 = register_user(email=uniq_email(), password='123', full_name='A')
    user2 = register_user(email=uniq_email(), password='123', full_name='B')

    assign_role(admin_id=admin, user_id=user1.id, role_name='admin')
    assign_role(admin_id=admin, user_id=user2.id, role_name='admin')

    result = active_users_for_role()

    assert result is not None

    roles = {r[0]: r[1] for r in result}
    assert roles.get('admin') >= 2


def test_users_without_profile(uniq_email):
    user = register_user(
        email=uniq_email(),
        password='123',
        full_name='A'
    )

    result = users_without_profile()
    user_ids = [u.id for u in result]

    assert user.id in user_ids


def test_group_by_registration_day(uniq_email):
    register_user(email=uniq_email(), password='123', full_name='A')
    register_user(email=uniq_email(), password='123', full_name='B')

    result = group_by_registration_day()

    assert result is not None
    assert len(result) > 0