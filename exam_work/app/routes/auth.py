from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from werkzeug.security import check_password_hash
from exam_work.app.repositories.user_repository import UserRepository
from exam_work.app.extensions import db

bp = Blueprint('auth', __name__, url_prefix='/auth')
user_repo = UserRepository(db)

login_manager = LoginManager()

def init_login_manager(app):
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для выполнения данного действия необходимо пройти процедуру аутентификации.'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return user_repo.get_user_by_id(user_id)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('animals.index'))

    if request.method == 'POST':
        login_input = request.form['login']
        password = request.form['password']
        remember = bool(request.form.get('remember'))

        user = user_repo.get_user_by_login(login_input)
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            flash('Вы успешно вошли в систему.', 'success')
            return redirect(url_for('animals.index'))
        else:
            flash('Невозможно аутентифицироваться с указанными логином и паролем.', 'danger')
            return render_template('login.html', login=login_input)

    return render_template('login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(request.referrer or url_for('animals.index'))
