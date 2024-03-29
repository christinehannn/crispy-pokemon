import os

from dotenv import load_dotenv

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from pokemon.config import Config

# Load environment variables
load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app():
    app = Flask(__name__)
    # app.config.from_object('pokemon.config.Config')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')

    db.init_app(app)

    # Create tables if not any
    import pokemon.models
    with app.app_context():
        db.create_all()

    bcrypt.init_app(app)
    login_manager.init_app(app)

    from pokemon.users.routes import users
    from pokemon.pokemons.routes import pokemons
    from pokemon.main.routes import main
    from pokemon.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(pokemons)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
