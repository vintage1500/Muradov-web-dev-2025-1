DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL 
) ENGINE INNODB;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(25) NOT NULL,
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(25) NOT NULL,
    middle_name VARCHAR(25) DEFAULT NULL,
    password_hash VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role_id INTEGER,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
) ENGINE INNODB;

CREATE TABLE visit_logs (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    path VARCHAR(100),
    user_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO roles (id, name)
VALUES (1, 'admin');

INSERT INTO roles (id, name)
VALUES (2, 'user');

INSERT INTO users (username, first_name, last_name, password_hash, role_id)
VALUES ('admin', 'Мурадов', 'Рауль', SHA2('qwerty', 256), 1);