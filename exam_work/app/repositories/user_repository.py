from app.models import User

class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user_by_login(self, login):
        return User.query.filter_by(username=login).first()

    def get_user_by_id(self, user_id):
        return User.query.get(user_id)
