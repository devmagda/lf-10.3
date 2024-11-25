from enum import Enum

import psycopg2
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user

import os
from dotenv import load_dotenv


from app.config import Config
from app.models import View, UserRole, User
from app.models.event import Event
from app.services import SessionManager, UserService, EventService, RoleService

# App Configurations
app = Flask(__name__)

app.config['SECRET_KEY'] = Config.SECRET_KEY

# Check if SECRET_KEY is loaded correctly
print("SECRET_KEY:", app.config['SECRET_KEY'])

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user_row = UserService.get_user_by_id(user_id)
    if user_row:
        return User(user_row[0], user_row[1], user_row[3])
    return None











@app.route('/view/<view_name>', methods=['POST'])
def set_view(view_name):
    try:
        view = View(view_name)
        SessionManager.set_view(view)
    except ValueError:
        return "Invalid view", 404  # Handle invalid view names

    # Redirect to a default page or a page based on the view
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
