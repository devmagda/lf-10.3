from flask import Blueprint, jsonify, request, Response, redirect, url_for, render_template
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from app.models import User, UserRole, View
from app.services import UserService, SessionManager, RoleService

auth_blueprint = Blueprint('auth', __name__, template_folder='./app/templates')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = UserService.get_user_by_username(username)

        if user and check_password_hash(user[2], password):
            user = User(user[0], user[1], user[3])
            login_user(user)
            SessionManager.set_user_role(UserRole.get_by_id(user.role))
            SessionManager.set_view(View.HOME)
            return redirect(url_for('index'))

        return "Login failed. Please try again.", 500

    return render_template('login.html')


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role_id = request.form['role_id']

        if UserService.user_exists(username):
            return "User already exists."

        UserService.create_user(username, password, role_id)

        SessionManager.set_view(View.LOGIN)

        return redirect(url_for('index'))

    selectable_roles = RoleService.get_selectable_roles()
    return render_template('register.html', selectable_roles=selectable_roles)


@auth_blueprint.route('/logout', methods=['POST'])
def logout():
    logout_user()
    SessionManager.set_user_role(UserRole.GUEST)
    SessionManager.set_view(View.HOME)
    return redirect(url_for('index'))
