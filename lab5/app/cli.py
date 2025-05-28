import click
from flask import current_app    
from .extension import db

@click.command('init-db')
def init_db_command():
    with db.engine.connect() as connection:
        with connection.begin():
            with current_app.open_resource('schema.sql') as f:
                raw_sql = f.read().decode('utf8')
                # Получаем низкоуровневое соединение (MySQLdb или mysql-connector)
                cursor = connection.connection.cursor()
                for _ in cursor.execute(raw_sql, multi=True):
                    pass
                cursor.close()
    click.echo('Initialized the database.')