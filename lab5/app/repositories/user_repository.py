from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, Role
from ..extension import db


class UserRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def get_by_id(self, user_id):
        return User.query.get(user_id)

    def get_by_username_and_password(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    def all(self):
        return db.session.query(User).outerjoin(Role).all()

    def create(self, username, password, first_name, middle_name, last_name, role_id):
        user = User(
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            role_id=role_id
        )
        user.set_password(password)  # Используем метод модели User
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user_id, first_name, middle_name, last_name, role_id):
        user = User.query.get(user_id)
        if user:
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name
            user.role_id = role_id
            db.session.commit()
        return user

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
        return user

    def check_old_password(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user:
            return check_password_hash(user.password_hash, password)
        return False

    def update_password(self, user_id, new_password):
        user = User.query.get(user_id)
        if user:
            user.set_password(new_password)
            db.session.commit()
        return user
