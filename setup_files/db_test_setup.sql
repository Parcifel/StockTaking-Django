CREATE DATABASE IF NOT EXISTS stocktaking;

USE stocktaking;

CREATE TABLE users (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE transaction_types (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL
);

CREATE TABLE stock (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE transactions (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER,
    stock_id INTEGER,
    transaction_type_id INTEGER,
    quantity INTEGER NOT NULL,
    date DATETIME NOT NULL
);

INSERT INTO users
    (username, password, active)
VALUE ('Aiden', 'password', TRUE);

INSERT INTO users
    (username, password, active)
VALUE ('Bella', 'password', TRUE);

INSERT INTO users
    (username, password, active)
VALUE ('Carter', 'password', TRUE);


INSERT INTO transaction_types
    (description)
VALUE ('add stock');

INSERT INTO transaction_types
    (description)
VALUE ('personal use');

INSERT INTO transaction_types
    (description)
VALUE ('sale');

INSERT INTO transaction_types
    (description)
VALUE ('correction');

INSERT INTO transaction_types
    (description)
VALUE ('loss');


INSERT INTO stock
    (description, quantity)
VALUE ('Pen', 10);

INSERT INTO stock
    (description, quantity)
VALUE ('Pencil', 5);

INSERT INTO stock
    (description, quantity)
VALUE ('Eraser', 3);