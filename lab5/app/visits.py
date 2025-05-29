from flask import Blueprint, render_template, request, send_file
from flask_login import current_user 
from .repositories.visit_repository import VisitLogRepository
from .extension import db
from .decorators import check_rights


visit_repository = VisitLogRepository(db)

bp = Blueprint('visits', __name__, url_prefix='/visits')


@bp.before_app_request
def log_visit():
    if request.endpoint and not request.path.startswith('/static'):
        visit_repository.log_visit(request.path, user_id=current_user.id if current_user.is_authenticated else None)


@bp.route('/')
@check_rights("view_logs_all")
def index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = visit_repository.get_all_paginated(page, per_page) 

    logs = []
    for idx, visit in enumerate(pagination.items, start=(page - 1) * per_page + 1):
        logs.append({
            'number': idx,
            'user': f"{visit.user.last_name} {visit.user.first_name} {visit.user.middle_name}" if visit.user else "Неаутентифицированный пользователь",
            'path': visit.path,
            'date': visit.created_at.strftime('%d.%m.%Y %H:%M:%S'),
        })

    return render_template('visits/main.html', logs=logs, pagination=pagination)

@bp.route('/user')
@check_rights("view_logs_own")
def index_user():
    page = request.args.get('page', 1, type=int)
    per_page = 10
 
    pagination = visit_repository.get_by_user_paginated(current_user.id, page, per_page)
    logs = []
    for idx, visit in enumerate(pagination.items, start=(page - 1) * per_page + 1):
        logs.append({
            'number': idx,
            'user': f"{visit.user.last_name} {visit.user.first_name} {visit.user.middle_name}",
            'path': visit.path,
            'date': visit.created_at.strftime('%d.%m.%Y %H:%M:%S'),
        })

    return render_template('visits/main.html', logs=logs, pagination=pagination)


@bp.route('/report/pages')
@check_rights("view_logs_all")
def report_by_pages():
    stats_raw = visit_repository.get_visits_grouped_by_path()
    stats = [{'path': row[0], 'count': row[1]} for row in stats_raw]
    return render_template('visits/report_pages.html', stats=stats)


@bp.route('/report/users')
@check_rights("view_logs_all")
def report_by_users():
    stats = visit_repository.get_visits_grouped_by_user()

    formatted_stats = []
    for i, (user_id, count) in enumerate(stats, start=1):
        user = visit_repository.get_user_by_id(user_id) if user_id else None
        try:
            name = user.last_name + " " + user.first_name + " " + user.middle_name if user else "Неаутентифицированный пользователь"
        except:
            name = user.last_name + " " + user.first_name if user else "Неаутентифицированный пользователь"
        formatted_stats.append((i, name, count))

    return render_template('visits/report_users.html', stats=formatted_stats)
 