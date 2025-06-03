from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from sqlalchemy import inspect
from app import User, db
from utils import requires_role

# localhost:5000/users
app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json
    user = User(
        username=data["username"],
        password=data["password"],
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "id": user.role_id,
                "name": user.role.name,
            },
        }
        for user in users
    ]

# # localhost:5000/
@app.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_role("admin")
def list_or_create_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}


@app.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
    }

# Diferença entre PATCH e PUT
# PATCH: Atualiza parcial (Atualiza só o title, só o body, só o datetime, só o author_id ou tudo, se quiser)
# PUT: Atualiza tudo (title, body, datetime e author_id)
# O PATCH é mais utilizado que o PUT

@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    # uma forma de fazer (versão mais simples)
    # if "username" in data:
    #     user.username = data["username"]
    #     db.session.commit()

    # outra forma de fazer (versão dinâmica melhorada)
    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
    }

@app.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT
