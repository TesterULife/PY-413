from sqlalchemy import select, func, cast, Date

from src.engine import sync_session_factory
from src.models.user import User
from src.models.role import Role
from src.models.profile import Profile


"""
10. Отчёты и метрики
Напишите запросы:

- Подсчитать число активных (неудалённых) пользователей по ролям.
- Получить список пользователей без профиля.
- Сгруппировать пользователей по дате регистрации 
    и вывести число регистраций за каждый день.
"""

def active_users_for_role():
    """
    SELECT role.name, COUNT(user.id) AS active_users FROM user
    JOIN roles
        ON role.id = user.role_id
    WHERE user.is_deleted = false
    GROUP BY role.name;
    """

    with sync_session_factory() as session:
        query = (
            select(
                Role.name,
                func.count(User.id.distinct()).label('active_users'),
            )
            .select_from(User)
            .join(User.roles)
            .where(User.is_deleted.is_(False))
            .group_by(Role.name)
        )

        result = session.execute(query)
        active_users = result.all()
        print(f'{active_users=}')


def users_without_profile():
    """
    SELECT * FROM user
    LEFT JOIN profiles
        ON user.id = profiles.user_id
    WHERE profiles.id IS NULL;
    """

    with sync_session_factory() as session:
        query = (
            select(User)
            .select_from(User)
            .outerjoin(User.profile)
            .where(Profile.id.is_(None))
        )

        result = session.execute(query)
        without_profile = result.scalars().all()
        print(f'{without_profile=}')


def group_by_registration_day():
    """
    SELECT DATE(joined_at), COUNT(*) FROM users
    GROUP BY DATE(joined_at)
    ORDER BY DATE(joined_at);
    """

    with sync_session_factory() as session:
        date_expr = cast(User.joined_at, Date)

        query = (
            select(
                date_expr.label('date_registration'),
                func.count(User.id).label('users_count'),
            )

            .select_from(User)
            .group_by('date_registration')
            .order_by('date_registration')
        )

        result = session.execute(query)
        registration_in_day = result.all()
        print(f'{registration_in_day=}')


