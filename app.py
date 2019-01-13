
# Verify if the application is being runned locally or in production.

from env_setup import env_keys
from flask import Flask
from flask_jwt_extended import JWTManager


keys = env_keys('SECRET_KEY', 'JWT_SECRET')

flask_app = Flask(__name__)


# Configure app
flask_app.config['JWT_SECRET_KEY'] = keys['JWT_SECRET']
flask_app.config['JWT_TOKEN_LOCATION'] = ['cookies']
flask_app.config['JWT_ACCESS_COOKIE_PATH'] = '/api'
flask_app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
flask_app.config['JWT_COOKIE_CSRF_PROTECT'] = True

jwt_app = JWTManager(flask_app)

# Blueprints
from blueprints.auth.main import auth_module

flask_app.register_blueprint(auth_module)

