from app.models import User

class UserRepository:
    def get_user_by_id(self, user_id):
        return User.query.get(user_id)