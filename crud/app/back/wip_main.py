from flask import Flask, request
import sqlite3


app = Flask(__name__)


def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE)"""
        )
        conn.commit()


@app.route("/", methods=["GET"])
def homepage():
    return {"message": "API is on"}, 200


@app.route("/users", methods=["POST"])
def create_user():
    payload = request.get_json()
    name, email = payload.get("name", None), payload.get("email", None)
    if not name or not email:
        msg = {
            "error": "Invalid payload, you need to declare keys name and email, shouldn't be null"
        }, 400
    else:
        try:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """INSERT INTO users (name, email) VALUES (?,?)""", (name, email)
                )
                conn.commit()
            msg = {"message": f"User added with success for email {email} "}, 201
        except Exception as e:
            msg = {"error": str(e)}, 500
    return msg


@app.route("/users", methods=["GET"])
def get_users():
    try:
        with get_db() as conn:
            conn.row_factory = sqlite3.Row
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


@app.route("/users/<string:user_id>", methods=["GET"])
def get_user_by_id(user_id: str):
    try:
        with get_db() as conn:
            conn.row_factory = sqlite3.Row
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


@app.route("/users/<string:user_id>", methods=["DELETE"])
def drop_user_by_id(user_id: str):
    with get_db() as conn:
        conn.row_factory = sqlite3.Row
        user_id_casted = int(user_id)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users where id={user_id_casted}")
        user = cursor.fetchall()
    if user:
        try:
            cursor.execute(f"DELETE FROM users where id={user_id_casted}")
            msg = {"message": f"User with id {user_id_casted} was deleted with success"}
        except Exception as e:
            msg = {"message": str(e)}
    else:
        msg = {"message": f"User id {user_id_casted} not found"}, 400

    return msg


@app.route("/users/<string:user_id>", methods=["PUT"])
def update_user_by_id(user_id: str):
    payload = request.get_json()
    if payload:
        name, email = payload.get("name", None), payload.get("email", None)
        with get_db() as conn:
            conn.row_factory = sqlite3.Row
            user_id_casted = int(user_id)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM users where id={user_id_casted}")
            user = cursor.fetchall()

        if user:
            if name and email:
                cursor.execute(
                    "UPDATE users SET name = ?, email = ? where id=?",
                    (name, email, user_id_casted),
                )
                msg = {
                    "message": f"Keys name and email changed for id {user_id_casted} with success"
                }, 200
            elif name and not email:
                cursor.execute(
                    "UPDATE users SET name = ?  where id= ?", (name, user_id_casted)
                )
                msg = {
                    "message": f"Key name changed for id {user_id_casted} with success"
                }, 200
            elif email and not name:
                cursor.execute(
                    "UPDATE users SET email = ? where id = ?", (email, user_id_casted)
                )
                msg = {
                    "message": f"Key email changed for id {user_id_casted} with success"
                }, 200

            else:
                msg = {
                    "error": "Isn't a valid payload, please declare name or email key to update"
                }, 500
        else:
            msg = {"error": "Invalid id"}, 500
    else:
        msg = {"mensage": "Payload is empty"}

    return msg


if __name__ == "__main__":
    # db_utils = DbUtils()
    # db_utils.init_db()
    init_db()
    app.run(host="127.0.0.1", port=5001, debug=True)
