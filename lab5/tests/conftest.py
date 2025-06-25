import pytest
from app import create_app, db as _db
from app.models import User, Role
from flask_login import login_user
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='session')
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
        'LOGIN_DISABLED': False,
        'SECRET_KEY': 'test',
    })

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def db(app):
    """Фикстура для базы данных. Очищает таблицы между тестами."""
    _db.session.begin_nested()

    yield _db

    _db.session.rollback()


@pytest.fixture(scope='function')
def client(app, db):
    """Тестовый клиент Flask."""
    return app.test_client()


@pytest.fixture
def admin_user(db):
    from app.models import Role, User

    # Очистка пользователей и ролей
    User.query.filter_by(username='admin').delete()
    Role.query.filter_by(id=1).delete()
    db.session.commit()

    role = Role(id=1, name='Администратор')
    db.session.add(role)
    db.session.commit()

    user = User(
        username='admin',
        first_name='Админ',
        last_name='Главный',
        password_hash=generate_password_hash('Admin123!'),
        role_id=1
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(scope='function')
def regular_user(db):
    # Очистка ролей перед созданием
    from app.models import Role, User

    User.query.filter_by(username='user').delete()
    Role.query.delete()
    db.session.commit()

    role = Role(id=2, name="Пользователь")
    db.session.add(role)
    db.session.commit()

    from app.models import User
    user = User(
        username='user',
        first_name='Обычный',
        middle_name='',
        last_name='Пользователь',
        role_id=2,
        password_hash=generate_password_hash('User123!')
    )
    db.session.add(user)
    db.session.commit()
    return user



def login(client, username, password):
    response = client.post('/auth/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)
    html = response.get_data(as_text=True)
    assert 'Выйти' in html or 'Авторизация прошла успешно' in html
    return response
