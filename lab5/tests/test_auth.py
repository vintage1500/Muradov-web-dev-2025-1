import pytest
from conftest import login


def test_login_success(client, admin_user):
    response = login(client, 'admin', 'Admin123!')
    assert 'Авторизация прошла успешно'.encode('utf-8') in response.data
    assert 'Выйти'.encode('utf-8') in response.data


def test_login_failure(client):
    response = login(client, 'wrong_user', 'wrong_password')
    assert 'Неверное имя пользователя или пароль'.encode('utf-8') in response.data


def test_logout(client, admin_user):
    login(client, 'admin', 'Admin123!')
    response = client.get('/auth/logout', follow_redirects=True)
    assert 'Войти'.encode('utf-8') in response.data


def test_protected_route_requires_login(client):
    response = client.get('/auth/update_password', follow_redirects=True)
    assert 'Авторизуйте для доступа к этому ресурсу'.encode('utf-8') in response.data or \
           'Войти'.encode('utf-8') in response.data


def test_update_password_success(client, admin_user):
    login(client, 'admin', 'Admin123!')
    response = client.post('/auth/update_password', data={
        'old_password': 'Admin123!',
        'new_password': 'NewPass123!',
        'confirm_password': 'NewPass123!'
    }, follow_redirects=True)
    assert 'Новый пароль сохранён'.encode('utf-8') in response.data


def test_update_password_wrong_old(client, admin_user):
    login(client, 'admin', 'Admin123!')
    response = client.post('/auth/update_password', data={
        'old_password': 'WrongOld',
        'new_password': 'NewPass123!',
        'confirm_password': 'NewPass123!'
    })
    assert 'Текущий пароль указан неверно'.encode('utf-8') in response.data


def test_update_password_weak(client, admin_user):
    login(client, 'admin', 'Admin123!')
    response = client.post('/auth/update_password', data={
        'old_password': 'Admin123!',
        'new_password': '12345678',
        'confirm_password': '12345678'
    })
    assert 'Пароль должен содержать строчные и заглавные буквы, цифры и быть без пробелов'.encode('utf-8') in response.data
