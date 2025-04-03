import re
from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

app = Flask(__name__)
application = app


app.config["SERVER_NAME"] = 'vintage150.pythonanywhere.com'   
# app.secret_key = '8806d05fdb32c6b25bbe417def4258c5e9b4dc4d865aa57a66105ce119d3da2e'
app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к секретной странице нужно пройти процедуру аутенфикации'
login_manager.login_message_category = 'warning'

def get_users():
    return [
        {
            'id': '1',
            'login': 'user',
            'password': 'qwerty'
        }
    ]


class User(UserMixin):
    def __init__(self, user_id, login):
        self.id = user_id
        self.login = login


@login_manager.user_loader
def load_user(user_id):
    for user in get_users():
        if user_id == user['id']:
            return User(user['id'], user['login'])
    return None


@app.route('/')
def index():
    msg = request.url
    return render_template('base.html', msg=msg)
 

@app.route('/counter')
def counter():
    if session.get('counter'):
        session['counter'] += 1
    else:
        session['counter'] = 1
    return render_template('counter.html')


@app.route('/login', methods=['GET', "POST"])
def login():
    next_page = request.args.get('next')
    if request.method == 'POST':
        login = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me') == 'on'
        if login and password:
            for user in get_users():
                if user['login'] == login and user['password'] == password:
                    user = User(user['id'], user['login'])
                    login_user(user, remember=remember_me)
                    flash('Вы успешно авторизованы', 'success')
                    return redirect(next_page or url_for('index'))
            return render_template('login.html', error='Пользователь не найден, проверьте корректность введенных данных. ')
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('Вы вышли из системы', 'exit')
    return redirect(url_for('index'))


@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')