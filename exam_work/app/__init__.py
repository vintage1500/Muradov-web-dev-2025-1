from flask import Flask, request, session
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app import models
from app.routes.auth import bp as auth_bp, init_login_manager
from app.routes.animals import bp as animals_bp
from app.routes.adoptions import bp as adoptions_bp

def handle_sqlalchemy_error(err):
    error_msg = 'Ошибка при подключении к базе данных. Повторите попытку позже.'
    return f'{error_msg} (Подробнее: {err})', 500

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate = Migrate(app, db)
    init_login_manager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(animals_bp)
    app.register_blueprint(adoptions_bp)

    app.errorhandler(SQLAlchemyError)(handle_sqlalchemy_error)

    return app