import click
from flask import current_app   
from flask.cli import with_appcontext
from .extension import db

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    with current_app.open_resource('schema.sql') as f:
        sql_script = f.read().decode('utf8')

        connection = db.connect()
        cursor = connection.cursor()
        
        # Разбиваем скрипт на отдельные команды и выполняем их
        for statement in sql_script.split(';'):
            if statement.strip():  # Пропускаем пустые строки
                cursor.execute(statement)
        
        connection.commit()
        cursor.close()
        click.echo('Initialized the database.')

        
        # with connection.cursor() as cursor:
        #     for _ in cursor.execute(f.read().decode('utf8'), multi=True):
        #         pass
        #     connection.commit()