import sqlite3
from models import DbUtils
from typing import Tuple, Dict


class Users:
    def __init__(self, db_utils: DbUtils):
        self.db_utils = db_utils

    def creating_user(self, name: str, email: str) -> Tuple[Dict, int]:
        if not name or not email:
            msg, status = {
                "error": "Invalid payload, you need to declare keys name and email, shouldn't be null"
            }, 400
        else:
            try:
                sql = "SELECT distinct email FROM users"
                emails_from_db = self.db_utils.execute_query(
                    sql=sql, sql_params=None, get_results=True
                )
                emails_list = [row[0] for row in emails_from_db]
                print("emails list", emails_list)
                if email not in emails_list:
                    sql = """INSERT INTO users (name, email) VALUES (?,?)"""
                    sql_params = (name, email)
                    self.db_utils.execute_query(
                        sql=sql, sql_params=sql_params, get_results=False
                    )
                    msg, status = {
                        "message": f"User added with success for email {email} "
                    }, 200

                else:
                    msg, status = {
                        "message": f"Email {email} used for another user "
                    }, 400
            except Exception as e:
                msg, status = {"error": str(e)}, 500
        return msg, status

    def getting_users(self) -> Tuple[Dict, int]:
        try:
            sql = "SELECT * FROM users"
            users = self.db_utils.execute_query(
                sql=sql, sql_params=None, get_results=True
            )
            if users:
                msg, status = [dict(user) for user in users], 200
            else:
                msg, status = {"message": "No users found"}, 400
        except Exception as e:
            msg, status = {"error": str(e)}, 500
        return msg, status

    def get_one_user_by_id(self, user_id: str) -> Tuple[Dict, int]:
        try:
            user_id_casted = int(user_id)
            sql = f"SELECT * FROM users where id={user_id_casted}"
            user = self.db_utils.execute_query(
                sql=sql, sql_params=None, get_results=True
            )
            if user:
                msg, status = dict(user[0]), 200
            else:
                msg, status = {"message": "No users found"}, 400
        except Exception as e:
            msg, status = {"error": str(e)}, 500
        return msg, status

    def delete_one_user_by_id(self, user_id: str) -> Tuple[Dict, int]:
        conn = self.db_utils.get_db()
        conn.row_factory = sqlite3.Row
        user_id_casted = int(user_id)
        sql = f"SELECT * FROM users where id={user_id_casted}"
        user = self.db_utils.execute_query(sql=sql, sql_params=None, get_results=True)
        if user:
            try:
                sql = f"DELETE FROM users where id={user_id_casted}"
                self.db_utils.execute_query(sql=sql, sql_params=None, get_results=False)
                msg, status = {
                    "message": f"User with id {user_id_casted} was deleted with success"
                }, 200
            except Exception as e:
                msg, status = {"message": str(e)}, 500
        else:
            msg, status = {"message": f"User id {user_id_casted} not found"}, 400

        return msg, status

    def updating_user_by_id(self, payload: dict, user_id: str) -> Tuple[Dict, int]:
        name, email = payload.get("name", None), payload.get("email", None)
        user_id_casted = int(user_id)
        sql_user = f"SELECT * FROM users where id={user_id_casted}"
        user = self.db_utils.execute_query(
            sql=sql_user, sql_params=None, get_results=True
        )
        sql_email = f"SELECT distinct email FROM users"
        emails_from_bd = self.db_utils.execute_query(
            sql=sql_email, sql_params=None, get_results=True
        )
        emails_list = [row[0] for row in emails_from_bd]

        if user:
            if name and email:
                if email in emails_list:
                    msg, status = {
                        "message": "This email is alread set by other user"
                    }, 400

                else:
                    sql = "UPDATE users SET name = ?, email = ? where id=?"
                    sql_params = (name, email, user_id_casted)
                    self.db_utils.execute_query(
                        sql=sql, sql_params=sql_params, get_results=False
                    )
                    msg, status = {
                        "message": f"Keys name and email changed for id {user_id_casted} with success"
                    }, 200
            elif name:
                sql = "UPDATE users SET name = ? where id= ?"
                sql_params = (name, user_id_casted)
                self.db_utils.execute_query(
                    sql=sql, sql_params=sql_params, get_results=False
                )
                msg, status = {
                    "message": f"Key name changed for id {user_id_casted} with success"
                }, 200
            elif email:
                if email in emails_list:
                    msg, status = {
                        "message": "This email is alread set by other user"
                    }, 400
                else:
                    sql = "UPDATE users SET email = ? where id = ?"
                    sql_params = (email, user_id_casted)
                    self.db_utils.execute_query(
                        sql=sql, sql_params=sql_params, get_results=False
                    )
                    msg, status = {
                        "message": f"Key email changed for id {user_id_casted} with success"
                    }, 200

            else:
                msg, status = {
                    "error": "Isn't a valid payload, please declare name or email key to update"
                }, 500
        else:
            msg, status = {"error": "Invalid id"}, 500

        return msg, status
