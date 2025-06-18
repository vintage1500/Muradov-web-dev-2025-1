from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required

from .extension import db
from .repositories import UserRepository

user_repository = UserRepository(db)

bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)
    login_manager.init_app(app)

def load_user(user_id):
    return user_repository.get_user_by_id(user_id)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')
        if login_input and password:
            user = user_repository.get_user_by_login(login_input)
            if user and user.check_password(password):
                login_user(user)
                flash('Вы успешно вошли в систему.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('main.index'))
        flash('Неверный логин или пароль.', 'danger')
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            flash('Пароли не совпадают.', 'danger')
        elif user_repository.get_user_by_login(login):
            flash('Пользователь с таким логином уже существует.', 'danger')
        else:
            user = user_repository.create_user(login, first_name, last_name, password)
            login_user(user)
            flash('Регистрация прошла успешно.', 'success')
            return redirect(url_for('main.index'))

    return render_template('auth/register.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('main.index'))
