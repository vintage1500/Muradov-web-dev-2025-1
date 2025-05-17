from functools import wraps
from flask import Blueprint, request, render_template, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from .repositories import UserRepository
from .extension import db


user_repository = UserRepository(db)

bp = Blueprint('auth', __name__, url_prefix='/auth')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Авторизуйте для доступа к этому ресурсу'
login_manager.login_message_category = 'warning'

class User(UserMixin):
    def __init__(self, user_data): 
        self.id = user_data['id']
        self.username = user_data['username']
        self.user_data = user_data  
        
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
            return redirect(request.args.get('next', url_for('index')))
            
        flash('Неверное имя пользователя или пароль', 'danger')
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.index'))
