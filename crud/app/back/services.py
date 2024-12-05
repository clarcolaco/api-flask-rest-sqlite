import sqlite3
from sqlite3 import Connection


class DbUtils:
    def __init__(self, database: str = "users.db"):
        self.database = database

    def get_db(self) -> Connection:
        conn = sqlite3.connect("users.db")
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


class Users:
    def __init__(self, db_utils: DbUtils):
        self.db_utils = db_utils

    def creating_user(self, name: str, email: str) -> dict:
        if not name or not email:
            msg = {
                "error": "Invalid payload, you need to declare keys name and email, shouldn't be null"
            }, 400
        else:
            try:
                conn = self.db_utils.get_db()  
                with conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        """INSERT INTO users (name, email) VALUES (?,?)""", (name, email)
                    )
                    conn.commit()
                    msg = {"message": f"User added with success for email {email} "}, 201
            except Exception as e:
                msg = {"error": str(e)}, 500
        return msg

    def getting_users(self) -> dict:
        try:
            conn = self.db_utils.get_db()  
            conn.row_factory = sqlite3.Row
            with conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
                users = cursor.fetchall()
                if users:
                    msg = [dict(user) for user in users], 200
                else:
                    msg = {"message": "No users found"}, 404
        except Exception as e:
            msg = {"error": str(e)}, 500
        return msg

    def get_one_user_by_id(self, user_id: str) -> dict:
        try:
            conn = self.db_utils.get_db()  
            conn.row_factory = sqlite3.Row
            with conn:
                user_id_casted = int(user_id)
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM users where id={user_id_casted}")
                conn.commit()
                user = cursor.fetchall()
                
                if user:
                    msg = dict(user[0]), 200
                else:
                    msg = {"message": "No users found"}, 404
        except Exception as e:
            msg = {"error": str(e)}, 500
        return msg

    def delete_one_user_by_id(self, user_id: str) -> dict:
        conn = self.db_utils.get_db() 
        conn.row_factory = sqlite3.Row
        user_id_casted = int(user_id)
        with conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users where id={user_id_casted}")
            user = cursor.fetchall()
            if user:
                try:
                    cursor.execute(f"DELETE FROM users where id={user_id_casted}")
                    msg = {
                        "message": f"User with id {user_id_casted} was deleted with success"
                    }, 200
                except Exception as e:
                    msg = {"message": str(e)}, 400
            else:
                msg = {"message": f"User id {user_id_casted} not found"}, 400

        return msg

    def updating_user_by_id(self, payload: dict, user_id: str) -> dict:

        name, email = payload.get("name", None), payload.get("email", None)
        conn = self.db_utils.get_db() 
        conn.row_factory = sqlite3.Row
        user_id_casted = int(user_id)

        with conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users where id={user_id_casted}")
            user = cursor.fetchall()

            if user:
                if name and email:
                    cursor.execute(
                        "UPDATE users SET name = ?, email = ? where id=?",
                        (name, email, user_id_casted)
                    )
                    msg = {
                        "message": f"Keys name and email changed for id {user_id_casted} with success"
                    }, 200
                elif name and not email:
                    cursor.execute("UPDATE users SET name = ? where id= ?", (name, user_id_casted))
                    msg = {
                        "message": f"Key name changed for id {user_id_casted} with success"
                    }, 200
                elif email and not name:
                    cursor.execute("UPDATE users SET email = ? where id = ?",(email, user_id_casted))
                    msg = {
                        "message": f"Key email changed for id {user_id_casted} with success"
                    }, 200

                else:
                    msg = {
                        "error": "Isn't a valid payload, please declare name or email key to update"
                    }, 500
            else:
                msg = {"error": "Invalid id"}, 500
        

        return msg
