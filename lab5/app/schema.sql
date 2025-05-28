-- DROP TABLE IF EXISTS users;
-- DROP TABLE IF EXISTS roles;
-- DROP TABLE IF EXISTS visit_logs;

-- CREATE TABLE roles (
--     id INTEGER PRIMARY KEY AUTO_INCREMENT,
--     name VARCHAR(25) NOT NULL 
-- ) ENGINE INNODB;

-- CREATE TABLE users (
--     id INTEGER PRIMARY KEY AUTO_INCREMENT,
--     username VARCHAR(25) NOT NULL,
--     first_name VARCHAR(25) NOT NULL,
--     last_name VARCHAR(25) NOT NULL,
--     middle_name VARCHAR(25) DEFAULT NULL,
--     password_hash VARCHAR(256) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     role_id INTEGER,
--     FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
-- ) ENGINE INNODB;

-- CREATE TABLE visit_logs (
--     id INTEGER PRIMARY KEY AUTO_INCREMENT,
--     path VARCHAR(100),
--     user_id INTEGER,
--     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
-- );

-- INSERT INTO roles (id, name)
-- VALUES (1, 'admin');

-- INSERT INTO roles (id, name)
-- VALUES (2, 'user');

-- INSERT INTO users (username, first_name, last_name, password_hash, role_id)
-- VALUES ('admin', 'Мурадов', 'Рауль', SHA2('qwerty', 256), 1);

/*
Для добавленя ролей и пользователей 
from app.models import db, User, Role

role_admin = Role(name='admin')
db.session.add(role_admin)
db.session.commit() 

role_user = Role(name='user')
db.session.add(role_user)
db.session.commit() 

user = User(username='admin', last_name='Мурадов', first_name='Рауль', role_id=1)
user.set_password('qwerty')
user.password_hash
db.session.add(user)
db.session.commit() 
*/