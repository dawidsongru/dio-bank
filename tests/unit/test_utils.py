from http import HTTPStatus

import pytest
from utils import eleva_quadrado, requires_role    # Importar os métodos


@pytest.mark.parametrize("test_input,expected", [(2, 4), (10, 100), (3, 9)])
def test_eleva_quadrado_sucesso(test_input, expected):
    resultado = eleva_quadrado(test_input)      # Executar o método
    assert resultado == expected                # Esperar o retorno


@pytest.mark.parametrize(
    "test_input,exc_class,msg",
    [
        ('a', TypeError, "unsupported operand type(s) for ** or pow(): 'str' and 'int'"),
        (None, TypeError, "unsupported operand type(s) for ** or pow(): 'NoneType' and 'int'")
    ]
)
def test_eleva_quadrado_falha(test_input, exc_class, msg):
    with pytest.raises(exc_class) as exc:
        eleva_quadrado(test_input)
        # breakpoint()
    assert str(exc.value) == msg
# Criando o método de teste
def test_requires_role_success(mocker):   # cenário de sucesso
    # Given (O que eu forneço para meu teste)
    mock_user = mocker.Mock()
    mock_user.role.name = "admin"

    mocker.patch("utils.get_jwt_identity")
    mocker.patch("utils.db.get_or_404", return_value=mock_user)
    decorated_function = requires_role("admin")(lambda: "success")

    # When (O que eu executo)
    result = decorated_function()

    # Then (O que eu verifico)
    assert result == "success"


def test_requires_role_fail(mocker):   # cenário de falha
    # Given (O que eu forneço para meu teste)
    mock_user = mocker.Mock()
    mock_user.role.name = "normal"

    # When (O que eu executo)
    mocker.patch("utils.get_jwt_identity")
    mocker.patch("utils.db.get_or_404", return_value=mock_user)
    decorated_function = requires_role("admin")(lambda: "success")
    
    result = decorated_function()
    
    # Then (O que eu verifico)
    assert result == ({"message": "User haven't access."}, HTTPStatus.FORBIDDEN)
