import os

SECRET_KEY = '8806d05fdb32c6b25bbe417def4258c5e9b4dc4d865aa57a66105ce119d3da2e'

MYSQL_USER = 'root'
MYSQL_PASSWORD = '12345678'
MYSQL_HOST = '127.0.0.1'
MYSQL_DATABASE = 'exam_work_db'

SQLALCHEMY_DATABASE_URI = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}/{MYSQL_DATABASE}"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    'static',
    'images'
)
