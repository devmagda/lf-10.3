from flask_login import UserMixin

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


class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    def is_admin(self):
        return self.role == UserRole.ADMIN

    def is_event_creator(self):
        return self.role == UserRole.CREATOR

    def is_user(self):
        return self.role == UserRole.USER

    def is_guest(self):
        return self.role == UserRole.GUEST
