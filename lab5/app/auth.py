from functools import wraps
from flask import Blueprint, request, render_template, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from .repositories import UserRepository
from .extension import db
import re

user_repository = UserRepository(db)

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Авторизуйте для доступа к этому ресурсу'
login_manager.login_message_category = 'warning'

class User(UserMixin):
    def __init__(self, user_data): 
        self.id = user_data.id  
        self.username = user_data.username
        self.first_name = user_data.first_name
        self.last_name = user_data.last_name
        self.middle_name = user_data.middle_name
        self.password_hash = user_data.password_hash
        self.created_at = user_data.created_at
        self.role_id = user_data.role_id
        self.role = user_data.role 
        
@login_manager.user_loader
def load_user(user_id):
    user = user_repository.get_by_id(user_id)
    if user: 
        return User(user) 
    return None

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('remember_me', None) == 'on'
        
        user = user_repository.get_by_username_and_password(username, password)
        
        if user:
            flash('Авторизация прошла успешно', 'success')
            login_user(User(user), remember=remember_me) 
            return redirect(request.args.get('next', url_for('users.index')))
            
        flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.index'))

@bp.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    problems = {}

    if request.method == 'POST':
        current_pwd = request.form.get('old_password')
        new_pwd = request.form.get('new_password')
        repeat_pwd = request.form.get('confirm_password')

        account = user_repository.get_by_id(current_user.id)

        # Проверка текущего пароля
        if not user_repository.check_old_password(account.username, current_pwd):
            problems['old_password'] = 'Текущий пароль указан неверно'

        # Проверка сложности нового пароля
        if not re.fullmatch(r'^(?=.*[a-zа-яё])(?=.*[A-ZА-ЯЁ])(?=.*\d)[^ ]+$', new_pwd or ''):
            problems['new_password'] = 'Пароль должен содержать строчные и заглавные буквы, цифры и быть без пробелов'
        elif not (8 <= len(new_pwd) <= 128):
            problems['new_password'] = 'Длина пароля должна быть от 8 до 128 символов'

        # Проверка совпадения паролей
        if new_pwd != repeat_pwd:
            problems['confirm_password'] = 'Введённые пароли не совпадают!'

        # Если всё хорошо — сохраняем
        if not problems:
            try:
                user_repository.update_password(account.id, new_pwd)
                flash('Новый пароль сохранён', 'success')
                return redirect(url_for('users.index'))
            except Exception:
                flash('Не удалось изменить пароль. Повторите позже', 'danger')
        else:
            return render_template('auth/update_password.html', errors=problems)

    return render_template('auth/update_password.html')