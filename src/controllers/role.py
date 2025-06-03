from http import HTTPStatus

from flask import Blueprint, request
from app import Role, db

# localhost:5000/users
app = Blueprint("role", __name__, url_prefix="/roles")


@app.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED
