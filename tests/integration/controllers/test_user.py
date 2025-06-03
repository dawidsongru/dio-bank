from http import HTTPStatus

from sqlalchemy import func
from app import Role, User, db

def test_get_user_success(client):              # Testando um comportamento de sucesso
    # Given (O que eu forneço para meu teste)
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="john-doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()

    # When (O que eu executo)
    response = client.get(f"/users/{user.id}")

    # Then (O que eu verifico)
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"id": user.id, "username": user.username}  # Verifica o conteúdo de retorno. Retorna id e username.

def test_get_user_not_found(client):            # Testando um comportamento de falha
    # Given (O que eu forneço para meu teste)
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user_id = 1

    # When (O que eu executo)
    response = client.get(f"/users/{user_id}")

    # Then (O que eu verifico)
    assert response.status_code == HTTPStatus.NOT_FOUND

def test_create_user(client, access_token):                  # Teste criar um novo usuário
    # Given (O que eu forneço para meu teste)
    # # role_id = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    # payload = {"username": "user2", "password": "user2", "role_id": 1}                # Criar os dados
    role_id = db.session.execute(db.select(Role.id).where(Role.name == "admin")).scalar()
    payload = {"username": "user2", "password": "user2", "role_id": role_id}                # Criar os dados

    # When (O que eu executo)
    response = client.post("/users/", json=payload, headers={"Authorization": f"Bearer {access_token}"})  # Endpoint que envia usuários (POST)

    # Then (O que eu verifico)
    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created!"}
    assert db.session.execute(db.select(func.count(User.id))).scalar() == 2

def test_list_users(client, access_token):                    # Teste list_user
    # Given (O que eu forneço para meu teste)
    user = db.session.execute(db.select(User).where(User.username == "john-doe")).scalar()
    response = access_token = client.post("/auth/login", json={"username": user.username, "password": user.password})
    access_token = response.json["access_token"]

    # When (O que eu executo)
    response = client.get("/users/", headers={"Authorization": f"Bearer {access_token}"})   # Endpoint que busca usuários (GET)
    
    # Then (O que eu verifico)
    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "role": {
                    "id": user.role_id,
                    "name": user.role.name,
                },
            }
        ]
    }
