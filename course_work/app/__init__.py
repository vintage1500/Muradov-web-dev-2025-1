from flask import Flask, session, request
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError

from .extension import db
from . import models
from app.auth import bp as auth_bp, init_login_manager
from app.routes import bp as main_bp
from app.catalogs import bp as catalog_bp
from app.cart import bp as cart_bp
from app.profile import bp as profile_bp
from app.admin import bp as admin_bp


def handle_sqlalchemy_error(err):
    error_msg = ('Возникла ошибка при подключении к базе данных. '
                 'Повторите попытку позже.')
    return f'{error_msg} (Подробнее: {err})', 500

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py', silent=False)

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate = Migrate(app, db)  
       
    init_login_manager(app)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    app.errorhandler(SQLAlchemyError)(handle_sqlalchemy_error)
   
    return app