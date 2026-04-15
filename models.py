import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'instance', 'minishop.db')


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT    NOT NULL UNIQUE,
            password TEXT    NOT NULL,
            role     TEXT    NOT NULL DEFAULT 'customer'
        );

        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            price       REAL    NOT NULL,
            description TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS orders (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity   INTEGER NOT NULL DEFAULT 1,
            status     TEXT    NOT NULL DEFAULT 'pending',
            FOREIGN KEY (user_id)    REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    ''')
    # Seed an admin account and sample products if empty
    if not db.execute('SELECT 1 FROM users WHERE role = "admin"').fetchone():
        from werkzeug.security import generate_password_hash
        db.execute(
            'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
            ('admin', generate_password_hash('admin123'), 'admin')
        )
    if not db.execute('SELECT 1 FROM products').fetchone():
        db.executemany(
            'INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
            [
                ('Laptop',     999.99, 'A powerful laptop'),
                ('Headphones',  49.99, 'Noise-cancelling headphones'),
                ('USB Hub',     19.99, 'Multi-port USB hub'),
            ]
        )
    db.commit()
    db.close()
