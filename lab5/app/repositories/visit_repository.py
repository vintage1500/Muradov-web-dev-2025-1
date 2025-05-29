from ..models import VisitLog, User
from sqlalchemy import func, desc
from datetime import datetime

class VisitLogRepository:
    def __init__(self, db_connector):
        self.db = db_connector

    def log_visit(self, path, user_id=None):
        visit = VisitLog(path=path, user_id=user_id)
        self.db.session.add(visit)
        self.db.session.commit()

    def get_all_paginated(self, page, per_page):
        return VisitLog.query.order_by(VisitLog.created_at.desc()).paginate(page=page, per_page=per_page)

    def get_by_user_paginated(self, user_id, page, per_page):
        return VisitLog.query.filter_by(user_id=user_id).order_by(VisitLog.created_at.desc()).paginate(page=page, per_page=per_page)

    def get_visits_grouped_by_path(self):
        return (
            self.db.session.query(
                VisitLog.path,
                func.count(VisitLog.id).label('count')
            )
            .group_by(VisitLog.path)
            .order_by(desc('count'))
            .all()
        )

    def get_visits_grouped_by_user(self):
        return (
            self.db.session.query(
                VisitLog.user_id,
                func.count(VisitLog.id).label('count')
            )
            .group_by(VisitLog.user_id)
            .order_by(desc('count'))
            .all()
        )

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)
