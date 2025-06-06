from functools import reduce
from collections import namedtuple
import logging
import pytest
import mysql.connector
from app import create_app
from app.db import DBConnector
from app.repositories.visit_repository import VisitRepository

TEST_DB_CONFIG = {
    'MYSQL_USER': 'root',
    'MYSQL_PASSWORD': '123',
    'MYSQL_HOST': 'localhost',
    'MYSQL_DATABASE': 'lab4_visit_tests',
}

def get_connection(app):
    return mysql.connector.connect(
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        host=app.config['MYSQL_HOST']
    )

def setup_db(app):
    logging.getLogger().info("Create test DB and schema...")
    db_name = app.config['MYSQL_DATABASE']
    create_query = (
        f"DROP DATABASE IF EXISTS {db_name};"
        f"CREATE DATABASE {db_name};"
        f"USE {db_name};"
    )

    with app.open_resource('schema.sql') as f:
        schema = f.read().decode('utf8')

    connection = get_connection(app)
    query = '\n'.join([create_query, schema])
    with connection.cursor(named_tuple=True) as cursor:
        for _ in cursor.execute(query, multi=True):
            pass
    connection.commit()
    connection.close()

def teardown_db(app):
    logging.getLogger().info("Drop test DB...")
    db_name = app.config['MYSQL_DATABASE']
    connection = get_connection(app)
    with connection.cursor() as cursor:
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name};")
    connection.close()

@pytest.fixture(scope="session")
def app():
    return create_app(TEST_DB_CONFIG)

@pytest.fixture(scope="session")
def db_connector(app):
    setup_db(app)
    with app.app_context():
        connector = DBConnector(app)
        yield connector
        connector.disconnect()
    teardown_db(app)

@pytest.fixture
def visit_repository(db_connector):
    return VisitRepository(db_connector)

@pytest.fixture
def clear_visit_logs(db_connector):
    with db_connector.connect().cursor() as cursor:
        cursor.execute("DELETE FROM visit_logs;")
        db_connector.connect().commit()
    yield

@pytest.fixture
def example_visits(db_connector):
    """Добавляет два примера посещений в таблицу visit_logs."""
    data = [
        (1, "home"),
        (2, "about"),
    ]
    row_class = namedtuple("Visit", ["id", "user_id", "page"])
    connection = db_connector.connect()
    with connection.cursor() as cursor:
        placeholders = ', '.join(['(%s, %s)' for _ in data])
        query = f"INSERT INTO visit_logs(user_id, page) VALUES {placeholders};"
        flat_data = reduce(lambda acc, tup: acc + list(tup), data, [])
        cursor.execute(query, flat_data)
        db_connector.connect().commit()

    with connection.cursor(named_tuple=True) as cursor:
        cursor.execute("SELECT id, user_id, page FROM visit_logs ORDER BY id ASC;")
        rows = cursor.fetchall()

    visits = [row_class(row.id, row.user_id, row.page) for row in rows]
    yield visits

    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM visit_logs;")
        db_connector.connect().commit()

@pytest.fixture
def client(app):
    return app.test_client()
