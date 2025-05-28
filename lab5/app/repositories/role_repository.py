from ..models import Role
from ..extension import db

class RoleRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def get_by_id(self, role_id):
        return Role.query.get(role_id)

    def get_all(self):
        return Role.query.all()
