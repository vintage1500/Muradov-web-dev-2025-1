from .extension import db
from datetime import datetime

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False) 

    # Связь с пользователями
    users = db.relationship('User', back_populates='role', cascade="all, delete", passive_deletes=True)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    middle_name = db.Column(db.String(25), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', ondelete='CASCADE'))

    # Связь с ролями
    role = db.relationship('Role', back_populates='users')
    # Связь с логами
    visit_logs = db.relationship('VisitLog', back_populates='user', cascade="all, delete", passive_deletes=True)


class VisitLog(db.Model):
    __tablename__ = 'visit_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    user = db.relationship('User', back_populates='visit_logs')
 