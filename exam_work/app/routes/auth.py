from flask import Blueprint
from app.extensions import login_manager
from app.models import User
from app.repositories.user_repository import UserRepository

bp = Blueprint('auth', __name__, url_prefix='/auth')
user_repo = UserRepository()

def init_login_manager(app):
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для выполнения данного действия необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return user_repo.get_user_by_id(user_id)
