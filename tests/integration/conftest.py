import pytest
from app import Role, User, create_app, db

@pytest.fixture()   # Método que cria e devolve o app
def app():
    app = create_app(
        {
            "SECRET_KEY": "test",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",     # O banco de dados vai rodar em memória, ele não vai criar...
            "JWT_SECRET_KEY": "test",                   #... um arquivo físico, ele vai armazenar tudo na memória.
        }
    )
    with app.app_context():
        db.create_all()             
        yield app
        # db.session.rollback()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture()
def access_token(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="john-doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    response = client.post("/auth/login", json={"username": user.username, "password": user.password})
    return response.json["access_token"]
