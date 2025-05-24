from functools import reduce
from collections import namedtuple
import logging
import pytest
import mysql.connector
from app import create_app
from app.db import DBConnector
from app.repositories import RoleRepository
from app.repositories import UserRepository

TEST_DB_CONFIG = {
    'MYSQL_USER': 'root',
    'MYSQL_PASSWORD': '12345678',
    'MYSQL_HOST': 'localhost',
    'MYSQL_DATABASE': 'lab4_test',
}

def get_connection(app):
    return mysql.connector.connect(
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        host=app.config['MYSQL_HOST']
    )

def setup_db(app):
    logging.getLogger().info("Create db...")
    test_db_name = app.config['MYSQL_DATABASE']
    create_db_query = (f'DROP DATABASE IF EXISTS {test_db_name}; '
                       f'CREATE DATABASE {test_db_name}; '
                       f'USE {test_db_name};')

    with app.open_resource('schema.sql') as f:
        schema_query = f.read().decode('utf8')

    connection = get_connection(app)
    query = '\n'.join([create_db_query, schema_query])
    with connection.cursor(named_tuple=True) as cursor:
        for _ in cursor.execute(query, multi=True):
                pass
    connection.commit()
    connection.close()


def teardown_db(app):
    logging.getLogger().info("Drop db...")
    test_db_name = app.config['MYSQL_DATABASE']
    connection = get_connection(app)
    with connection.cursor() as cursor:
        cursor.execute(f'DROP DATABASE IF EXISTS {test_db_name};')
    connection.close()

    
@pytest.fixture(autouse=True)
def cleanup_tables(db_connector):
    """Очищает таблицы users и roles перед каждым тестом, чтобы избежать конфликтов FK"""
    connection = db_connector.connect()
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM users;")
        cursor.execute("DELETE FROM roles;")
        connection.commit()


@pytest.fixture(scope='session')
def app():
    return create_app(TEST_DB_CONFIG)

@pytest.fixture(scope='session')
def db_connector(app):
    setup_db(app)
    with app.app_context():
        connector = DBConnector(app)
        yield connector
        connector.disconnect()
    teardown_db(app)

@pytest.fixture
def role_repository(db_connector):
    return RoleRepository(db_connector)

@pytest.fixture
def user_repository(db_connector):
    return UserRepository(db_connector)

@pytest.fixture
def existing_role(db_connector):
    data = (1, 'admin')
    row_class = namedtuple('Row', ['id', 'name'])
    role = row_class(*data)

    connection = db_connector.connect()
    
    with connection.cursor() as cursor:
        query = 'INSERT INTO roles(id, name) VALUES (%s, %s);'
        cursor.execute(query, data)
        connection.commit()

    yield role

    with connection.cursor() as cursor:
        query = 'DELETE FROM roles WHERE id=%s;'
        cursor.execute(query, (role.id,))
        connection.commit()

@pytest.fixture
def nonexisting_role_id():
    return 1

@pytest.fixture
def example_roles(db_connector):
    data = [(1, 'admin'), (2, 'test')]
    row_class = namedtuple('Row', ['id', 'name'])
    roles = [row_class(*row_data) for row_data in data]

    connection = db_connector.connect()

    with connection.cursor() as cursor:
        placeholders = ', '.join(['(%s, %s)' for _ in range(len(data))])
        query = f"INSERT INTO roles(id, name) VALUES {placeholders};"
        cursor.execute(query, reduce(lambda seq, x: seq + list(x), data, []))
        connection.commit()

    yield roles

    with connection.cursor() as cursor:
        role_ids = ', '.join([str(role.id) for role in roles])
        query = f"DELETE FROM roles WHERE id IN ({role_ids});"
        cursor.execute(query)
        connection.commit()

@pytest.fixture
def existing_users(db_connector, example_roles):
    users_data = [
        (1, 'user1', 'password1', 'Raul', 'Muradov', 'RR', 1),
        (2, 'user2', 'password2', 'Yana', 'Forshteer', 'MM', 2),
    ]
    row_class = namedtuple('Row', ['id', 'username', 'password_hash', 'first_name', 'middle_name', 'last_name', 'role_id'])
    users = [row_class(*user_data) for user_data in users_data]

    connection = db_connector.connect()
    with connection.cursor() as cursor:
        placeholders = ', '.join(['(%s, %s, SHA2(%s, 256), %s, %s, %s, %s)' for _ in range(len(users_data))])
        query = f"INSERT INTO users(id, username, password_hash, first_name, middle_name, last_name, role_id) VALUES {placeholders};"
        cursor.execute(query, reduce(lambda seq, x: seq + list(x), users_data, []))
        connection.commit()

    yield users

    with connection.cursor() as cursor:
        user_ids = ', '.join([str(user.id) for user in users])
        query = f"DELETE FROM users WHERE id IN ({user_ids});"
        cursor.execute(query)
        connection.commit()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def logged_in_user(client, existing_users):
    # Логиним пользователя перед тестами смены пароля
    with client:
        client.post('/login', data={
            'username': existing_users[0].username,
            'password': 'password1'
        })
        yield

@pytest.fixture
def login_existing_user(client, existing_users):
    with client.session_transaction() as session:
        session['_user_id'] = str(existing_users[0].id)