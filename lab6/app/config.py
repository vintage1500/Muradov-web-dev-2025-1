import os

SECRET_KEY = 'secret-key'

# SQLALCHEMY_DATABASE_URI = 'sqlite:///project.db'
# SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:12345678@localhost/lab6'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://vintage150:Qwerty123!@vintage150.mysql.pythonanywhere-services.com/vintage150$lab6'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..',
    'media',
    'images'
)