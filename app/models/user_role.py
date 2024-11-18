from enum import Enum


class UserRole(Enum):
    ADMIN = 3
    CREATOR = 2
    USER = 1
    GUEST = 0

    @staticmethod
    def get_by_id(role_id):
        for role in UserRole:
            if role.value == role_id:
                return role
        raise ValueError(f"Invalid role ID: {role_id}")
