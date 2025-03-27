import pytest
from flask import url_for, session
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_url_params(client):
    response = client.get('/params?name=Raul&age=22')
    assert b'name' in response.data
    assert b'Raul' in response.data
    assert b'age' in response.data
    assert b'22' in response.data


def test_url_params_display(client):
    response = client.get('/params?name=Same&age=25&city=Moscow')
    assert response.status_code == 200

    expected_params = {
        "name": "Same",
        "age": "25",
        "city": "Moscow"
    }

    for key, value in expected_params.items():
        assert key.encode() in response.data
        assert value.encode() in response.data
         
def test_headers(client):
    response = client.get('/headers')
    assert response.status_code == 200
    assert b'User-Agent' in response.data 

def test_headers_display(client):
    response = client.get('/headers', headers={
        'User-Agent': 'TestClient/1.0',
        'Accept': 'text/html',
        'X-Custom-Header': 'CustomValue'
    })
    assert response.status_code == 200
    assert b'User-Agent' in response.data
    assert b'TestClient/1.0' in response.data
    assert b'Accept' in response.data
    assert b'text/html' in response.data
    assert b'X-Custom-Header' in response.data
    assert b'CustomValue' in response.data
 
def test_cookies(client):
    client.get('/cookies')  
    response = client.get('/cookies')  
    assert response.status_code == 200
    assert b'<td>name</td>' in response.data
    assert b'<td>Same</td>' in response.data
    # delete
    response = client.get('/cookies')
    assert b'<td>name</td>' not in response.data
    assert b'<td>Same</td>' not in response.data
 
def test_form_get(client):
    response = client.get('/form')
    assert response.status_code == 200
    assert b'<form method="POST">' in response.data


def test_form_post(client):
    response = client.post('/form', data={'theme': 'Test', 'text': 'Hello'})
    assert response.status_code == 200
    assert b'theme' in response.data
    assert b'Test' in response.data
    assert b'text' in response.data
    assert b'Hello' in response.data
 
def test_phone_form_invalid_chars(client):
    response = client.post('/phone', data={'phone': 'abc123'})
    assert response.status_code == 200
    assert 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'.encode('utf-8') in response.data
    assert b'is-invalid' in response.data
    assert b'invalid-feedback"' in response.data

def test_phone_form_invalid_length(client):
    response = client.post('/phone', data={'phone': '12345'})
    assert response.status_code == 200
    assert 'Недопустимый ввод. Неверное количество цифр.'.encode('utf-8') in response.data
    assert b'is-invalid' in response.data
    assert b'invalid-feedback' in response.data

def test_phone_form_valid1(client):
    response = client.post('/phone', data={'phone': '8(999)123-45-67'})
    assert response.status_code == 200
    assert b'8-999-123-45-67' in response.data


def test_phone_form_valid2(client):
    response = client.post('/phone', data={'phone': ' +7 (123) 456-75-90'})
    assert response.status_code == 200
    assert b'8-123-456-75-90' in response.data

def test_phone_form_valid3(client):
    response = client.post('/phone', data={'phone': ' 123.456.75.90'})
    assert response.status_code == 200
    assert b'8-123-456-75-90' in response.data

def test_phone_form_valid4(client):
    response = client.post('/phone', data={'phone': ' 123-456-75-90'})
    assert response.status_code == 200
    assert b'8-123-456-75-90' in response.data

def test_phone_form_valid5(client):
    response = client.post('/phone', data={'phone': '8-123-456-75-90'})
    assert response.status_code == 200
    assert b'8-123-456-75-90' in response.data
    
def test_phone_form_page_load(client):
    response = client.get('/phone')
    assert response.status_code == 200
    assert b'<form' in response.data    
    assert b'name="phone"' in response.data