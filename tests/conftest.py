# import sys
# import os

# # Caminho absoluto até a pasta 'src'
# src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dio_bank', 'src'))

# # Adiciona ao sys.path se ainda não estiver
# if src_path not in sys.path:
#     sys.path.insert(0, src_path)

import sys
import os
import pytest

# Caminho absoluto até a pasta 'src'
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dio_bank', 'src'))

# Adiciona ao sys.path se ainda não estiver
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from app import create_app

@pytest.fixture
def client():
    app = create_app()  # Ou apenas 'app' se você não usa factory
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
