from flask_login import current_user
import pytest
from conftest import login
from app.repositories import VisitLogRepository


def test_visit_logging(client, admin_user):
    login(client, 'admin', 'Admin123!')
    client.get('/users/', follow_redirects=True)

    logs = VisitLogRepository(client.application.extensions['db']).get_all_paginated(1, 10).items
    assert any('/users/' in log.path for log in logs)


def test_admin_can_view_all_visits(client, admin_user):
    login(client, 'admin', 'Admin123!')
    response = client.get('/visits/', follow_redirects=True)
    assert 'Журнал посещений' in response.get_data(as_text=True)
    assert 'Пользователь'.encode('utf-8') in response.data


def test_regular_user_sees_only_their_visits(client, regular_user):
    login(client, 'user', 'User123!')
    response = client.get('/visits/user', follow_redirects=True)
    assert 'Журнал посещений'.encode('utf-8') in response.data


def test_regular_user_cannot_see_all_visits(client, regular_user):
    login(client, 'user', 'User123!')
    response = client.get('/visits/', follow_redirects=True)
    assert 'У вас недостаточно прав'.encode('utf-8') in response.data


def test_report_by_pages_view(client, admin_user):
    login(client, admin_user.username, 'Admin123!')

    with client.application.test_request_context():
        # Проверка на месте
        assert current_user.is_authenticated
        assert current_user.role_id == 1, f"role_id={current_user.role_id}, expected=1"

    response = client.get('/visits/report/pages', follow_redirects=True)
    html = response.get_data(as_text=True)
    print(html)
    assert 'Отчёт по посещениям страниц' in html


def test_report_by_pages_csv(client, admin_user):
    login(client, admin_user.username, 'Admin123!')
    response = client.get('/visits/report/pages/export', follow_redirects=True)
    assert response.status_code == 200
    assert 'report_by_pages.csv' in response.headers.get('Content-Disposition', '')


def test_report_by_users_view(client, admin_user):
    login(client, admin_user.username, 'Admin123!')
    response = client.get('/visits/report/users', follow_redirects=True)
    html = response.get_data(as_text=True)
    assert 'Отчёт: посещения по пользователям' in html


def test_report_by_users_csv(client, admin_user):
    login(client, admin_user.username, 'Admin123!')
    response = client.get('/visits/report/users/export', follow_redirects=True)
    assert response.status_code == 200
    assert 'report_by_users.csv' in response.headers.get('Content-Disposition', '')