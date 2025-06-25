from datetime import datetime
from exam_work.app.extensions import db
from flask_login import UserMixin

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    patronymic = db.Column(db.String(64))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    role = db.relationship('Role', backref='users')

class Animal(db.Model):
    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    description = db.Column(db.Text, nullable=False)
    age_months = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    photos = db.relationship('Photo', backref='animal', cascade='all, delete')
    adoptions = db.relationship('Adoption', backref='animal', cascade='all, delete')

class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    mime_type = db.Column(db.String(64), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False)

class Adoption(db.Model):
    __tablename__ = 'adoptions'

    id = db.Column(db.Integer, primary_key=True)
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    contact_info = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Date, default=datetime.utcnow)
    status = db.Column(db.String(32), nullable=False, default='pending')

    user = db.relationship('User', backref='adoptions') 