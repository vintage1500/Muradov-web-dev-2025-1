class RoleRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector
        
    def get_by_id(self, role_id):
        with self.db_connector.connect().cursor(dictionary=True) as cursor: 
            cursor.execute("SELECT * FROM roles WHERE id = %s;", (role_id,))
            return cursor.fetchone()
        
    def get_all(self):
        with self.db_connector.connect().cursor(dictionary=True) as cursor: 
            cursor.execute("SELECT * FROM roles")
            return cursor.fetchall()