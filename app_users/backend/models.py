from sqlite3 import Connection
import sqlite3

class DbUtils:
    def __init__(self, database:str) -> None:
        self.database = database

    def get_db(self) -> Connection:
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        conn = self.get_db()
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                email TEXT NOT NULL UNIQUE)"""
        )
        conn.commit()
