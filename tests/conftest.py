import pytest
import os

from tests.db.DBContextManager import DBTestContextManager
from tests.db.DBConnection.db_connection_manajer import db_connection
from tests.db.TestDB import TestDB

# Configurar logging para que muestre solo los errores
import logging
logging.getLogger().handlers.clear()  # Para evitar que se dupliquen los logs
logging.getLogger().level = logging.INFO
# Si se quiere ver los queries, cambiar a INFO
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

DB_PATH = os.path.join('tests/tools/db/test.db')


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    if os.path.exists(DB_PATH):
        logging.info(f"DB {DB_PATH} already exists")
        return
    db_connection.drop_tables()
    db_connection.create_tables()
    TestDB().setup_data()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture(scope='function')
def test_session():
    """
    Fixture que proporciona una sesión de base de datos gestionada con 'with'.
    """
    with DBTestContextManager() as session:
        yield session