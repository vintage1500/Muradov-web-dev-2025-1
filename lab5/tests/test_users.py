import pytest
from flask import url_for

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def test_user_list_access_admin(client, admin_user):
    login(client, admin_user.username, 'adminpass')
    response = client.get(url_for('users.index'))
    assert 'Добавить нового пользователя'.encode('itf-8') in response.data
    assert 'Удалить'.encode('itf-8') in response.data

def test_user_list_access_user(client, regular_user):
    login(client, regular_user.username, 'userpass')
    response = client.get(url_for('users.index'))
    assert 'Изменить'.encode('itf-8') not in response.data
    assert 'Удалить'.encode('itf-8') not in response.data

def test_empty_user_list(client, admin_user, db_session):
    # Очистим таблицу пользователей
    db_session.query(User).delete()
    db_session.commit()
    login(client, admin_user.username, 'adminpass')
    response = client.get(url_for('users.index'))
    assert 'Нет зарегистрированных пользователей'.encode('itf-8') in response.data
