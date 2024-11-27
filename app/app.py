from flask import Flask
from flask_login import LoginManager

from app.models import User
from app.services import UserService
from app.config import Config
from app.routes import events_blueprint, roles_blueprint, auth_blueprint, global_blueprint, views_blueprint

def create_app():
    flaskr = Flask(__name__)
    flaskr.config.from_object('app.config.Config')

    flaskr.config['SECRET_KEY'] = Config.SECRET_KEY

    # Check if SECRET_KEY is loaded correctly
    print("SECRET_KEY:", flaskr.config['SECRET_KEY'])

    flaskr.template_folder = 'templates'
    flaskr.static_folder = 'static'

    login_manager = LoginManager()
    login_manager.init_app(flaskr)

    @login_manager.user_loader
    def load_user(user_id):
        user_row = UserService.get_user_by_id(user_id)
        if user_row:
            return User(user_row[0], user_row[1], user_row[3])
        return None

    # Register Blueprints
    flaskr.register_blueprint(auth_blueprint)
    flaskr.register_blueprint(roles_blueprint)
    flaskr.register_blueprint(global_blueprint)
    flaskr.register_blueprint(views_blueprint, url_prefix='/view')
    flaskr.register_blueprint(events_blueprint, url_prefix='/events')

    return flaskr