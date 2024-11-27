from flask import Request
from werkzeug.security import generate_password_hash

from app.models.user import User
from . import ConnectionUtil

connection = ConnectionUtil.from_global_config()


class UserService:
    @staticmethod
    def get_user_by_id(user_id):
        cursor = connection.db.cursor()
        cursor.execute("SELECT * FROM tbl_users WHERE id = %s", (user_id,))
        user_row = cursor.fetchone()
        cursor.close()
        return user_row

    @staticmethod
    def get_user_by_username(username):
        cursor = connection.db.cursor()
        cursor.execute("SELECT * FROM tbl_users WHERE username = %s", (username,))
        user_row = cursor.fetchone()
        cursor.close()
        return user_row

    @staticmethod
    def user_exists(username):
        user = UserService.get_user_by_username(username)
        return user is not None

    @staticmethod
    def create_user(username, password, role_id):
        hashed_password = generate_password_hash(password)
        cursor = connection.db.cursor()
        cursor.execute("INSERT INTO tbl_users (username, password, role_id) VALUES (%s, %s, %s)",
                       (username, hashed_password, role_id))
        connection.db.commit()
        cursor.close()

    @staticmethod
    def get_user(request: Request):
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role_id']

        return User(username, password, role_id)
