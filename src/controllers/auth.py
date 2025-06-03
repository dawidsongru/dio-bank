from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from sqlalchemy import inspect
from app import User, db

app = Blueprint("auth", __name__, url_prefix="/auth")


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = db.session.execute(
        db.select(User).where(User.username == username)
    ).scalar_one_or_none()

    if not user or user.password != password:
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    # JWT identity deve ser string
    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}
