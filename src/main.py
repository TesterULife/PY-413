from src.queries.orm import (
    active_users_for_role,
    users_without_profile,
    group_by_registration_day
)


def main():
    print("=== Active users by role ===")
    for role, count in active_users_for_role():
        print(f"{role}: {count}")

    print("\n=== Users without profile ===")
    for user in users_without_profile():
        print(f"{user.id} | {user.email}")

    print("\n=== Registrations by day ===")
    for day, count in group_by_registration_day():
        print(f"{day}: {count}")


if __name__ == "__main__":
    main()