from flask_login import UserMixin
from enum import Enum


class UserRole(Enum):
    ADMIN: int = 3
    CREATOR: int = 2
    USER: int = 1
    GUEST: int = 0

    @staticmethod
    def get_by_id(role_id: int) -> "UserRole":
        for role in UserRole:
            if role.value == role_id:
                return role
        raise ValueError(f"Invalid role ID: {role_id}")


class User(UserMixin):
    id: int
    username: str
    role: UserRole

    def __init__(self, id: int, username: str, role: UserRole) -> None:
        self.id = id
        self.username = username
        self.role = role

    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def is_event_creator(self) -> bool:
        return self.role == UserRole.CREATOR

    def is_user(self) -> bool:
        return self.role == UserRole.USER

    def is_guest(self) -> bool:
        return self.role == UserRole.GUEST
