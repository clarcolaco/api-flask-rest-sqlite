from sqlite3 import Connection
import sqlite3


class DbUtils:
    def __init__(self, database: str) -> None:
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

    def execute_query(self, sql: str, sql_params: tuple, get_results: bool) -> any:
        try:
            conn = self.get_db()
            with conn:
                cursor = conn.cursor()
                if get_results and not sql_params:
                    cursor.execute(sql)
                    conn.commit()
                    return cursor.fetchall()
                if not get_results and not sql_params:
                    cursor.execute(sql)
                    conn.commit()
                else:
                    cursor.execute(sql, sql_params)
                    conn.commit()
                    return None
        except Exception as e:
            print(f"Connection with db failed {e}")
        finally:
            conn.close()
