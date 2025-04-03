import pytest
from flask import url_for, session
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client
 

def test_counter(client):
    """Cчетчик посещений.""" 
    res1 = client.get('/counter')
    assert 'Вы посетили данную таблицу 1 раз!'.encode('utf-8') in res1.data
    
    res2 = client.get('/counter')
    assert 'Вы посетили данную таблицу 2 раз!'.encode('utf-8') in res2.data

def test_successful_login(client):
    """Успешный вход в систему"""
    response = client.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)    
    assert 'Вы успешно авторизованы'.encode('utf-8') in response.data  # Проверка flash-сообщения

def test_unsuccessful_login(client):
    """Неуспешный вход в систему"""
    response = client.post('/login', data={'username': 'user', 'password': 'wrong'}, follow_redirects=True)
    assert 'Пользователь не найден'.encode('utf-8') in response.data  # Ошибочное сообщение

def test_authenticated_user_access_secret(client):
    """Аутентифицированный пользователь секрет"""
    client.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
    response = client.get('/secret')
    assert 'Вы смогли попасть на эту страничку'.encode('utf-8') in response.data

def test_anonymous_user_redirected_from_secret(client):
    """Неаутентифицированный пользователь отказ секрет -> страница входа."""
    response = client.get('/secret', follow_redirects=True)
    assert 'Для доступа к секретной странице нужно пройти процедуру аутенфикации'.encode('utf-8') in response.data

def test_redirect_after_login(client):
    """Перенаправление секрет"""
    response = client.get('/secret', follow_redirects=False)
    assert response.status_code == 302
    login_url = response.headers['Location']
    response = client.post(login_url, data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
    assert 'Вы смогли попасть на эту страничку'.encode('utf-8') in response.data  # Успешный доступ после входа

def test_remember_me(client):
    """Запомнить меня"""
    response = client.post('/login', data={'username': 'user', 'password': 'qwerty', 'remember_me': 'on'})
    assert 'remember_token' in response.headers.get('Set-Cookie', '')

def test_navbar_authenticated(client):
    """Навбар аутентифицированный пользователь"""
    client.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
    response = client.get('/')
    assert 'Секрет'.encode('utf-8') in response.data
    assert 'Выйти'.encode('utf-8') in response.data
    assert 'Войти'.encode('utf-8') not in response.data

def test_navbar_anonymous(client):
    """Навбар неаутентифицированный пользователь"""
    response = client.get('/')
    assert 'Секрет'.encode('utf-8') not in response.data
    assert 'Выйти'.encode('utf-8') not in response.data
    assert 'Войти'.encode('utf-8') in response.data

def test_logout(client):
    """Выход из системы""" 
    client.post('/login', data={'username': 'user', 'password': 'qwerty'}, follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert 'Вы вышли из системы'.encode('utf-8') in response.data 