from app.models import User
from werkzeug.security import generate_password_hash

class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_all_users(self):
        return self.db.session.execute(self.db.select(User)).scalars()

    def get_user_by_id(self, user_id):
        return self.db.session.execute(self.db.select(User).filter_by(id=user_id)).scalar()

    def get_user_by_login(self, login):
        return self.db.session.execute(self.db.select(User).filter_by(login=login)).scalar()

    def create_user(self, login, first_name, last_name, password):
        user = User(
            login=login,
            first_name=first_name,
            last_name=last_name,
            password_hash=generate_password_hash(password)
        )
        self.db.session.add(user)
        self.db.session.commit()
        return user