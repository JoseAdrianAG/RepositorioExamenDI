import sqlite3
import os

class Database:
    def __init__(self, db_name="users.db"):
        db_name = os.path.join(os.path.dirname(__file__), 'users.db')
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_user(self, name, password, role):
        self.cursor.execute("INSERT INTO users (name, password, role) VALUES (?, ?, ?)", (name, password, role))
        self.conn.commit()

    def update_user(self, user_id, name, password, role):
        self.cursor.execute("UPDATE users SET name=?, password=?, role=? WHERE id=?", (name, password, role, user_id))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
        self.conn.commit()

    def get_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()
