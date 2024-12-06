from flask import Flask, request
from controllers import  Users
from models import DbUtils
from typing import Tuple 
import os


IS_DOCKER = os.getenv("IS_DOCKER", "false").lower() == "true"
HOST = "0.0.0.0" if IS_DOCKER else "127.0.0.1"



app = Flask(__name__)


@app.route("/", methods=["GET"])
def homepage() -> Tuple[dict, int]:
    response, status_code = {"message": "API is on"}, 200
    return response, status_code


@app.route("/users", methods=["POST"])
def create_user() -> Tuple[dict, int]:
    payload = request.get_json()
    name, email = payload.get("name", None), payload.get("email", None)
    response, status_code = Users(db_utils).creating_user(name=name, email=email)
    return response, status_code


@app.route("/users", methods=["GET"])
def get_users() -> Tuple[dict, int]:
    response, status_code = Users(db_utils).getting_users()
    return response, status_code


@app.route("/users/<string:user_id>", methods=["GET"])
def get_user_by_id(user_id: str) -> Tuple[dict, int]:
    response, status_code = Users(db_utils).get_one_user_by_id(user_id=user_id)
    return response, status_code


@app.route("/users/<string:user_id>", methods=["DELETE"])
def drop_user_by_id(user_id: str) -> Tuple[dict, int]:
    response, status_code = Users(db_utils).delete_one_user_by_id(user_id=user_id)
    return response, status_code


@app.route("/users/<string:user_id>", methods=["PUT"])
def update_user_by_id(user_id: str) -> Tuple[dict, int]:
    payload = request.get_json()
    if payload:
        response, status_code = Users(db_utils).updating_user_by_id(
        payload=payload, user_id=user_id
    )
    else:
        response, status_code = {"mensage": "Payload is empty"}, 400
    return response, status_code


if __name__ == "__main__":
    db_utils = DbUtils("sqlite.db")
    db_utils.init_db()
    app.run(host=HOST, port=5001, debug=True)
