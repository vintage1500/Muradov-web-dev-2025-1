DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;

CREATE TABLE roles {
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL,
    description TEXT
} ENGINE INNODB;

CREATE TABLE users {
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(25) NOT NULL,
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(25) NOT NULL,
    middle_name VARCHAR(25) DEFAULT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT TIMESTAMP,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(id)
} ENGINE INNODB;

INSERT INTO roles(id, name)
VALUES (1, 'admin');

INSERT INTO users(username, first_name, last_name, password_hash, role_id)
VALUES ('admin', 'Мурадов', 'Рауль', SHA2('qwerty', 256), 1);