from flask import Flask
from flask_login import LoginManager

from .config import Config
from .routes import events_blueprint, roles_blueprint, auth_blueprint, global_blueprint
app = Flask(__name__)
app.config.from_object('app.config.Config')

app = Flask(__name__)

app.config['SECRET_KEY'] = Config.SECRET_KEY

# Check if SECRET_KEY is loaded correctly
print("SECRET_KEY:", app.config['SECRET_KEY'])

app.template_folder = 'templates'

#login_manager = LoginManager()
#login_manager.init_app(app)

# Register Blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(roles_blueprint)
app.register_blueprint(global_blueprint)
app.register_blueprint(events_blueprint, url_prefix='/events')

if __name__ == "__main__":
    app.run(debug=True)