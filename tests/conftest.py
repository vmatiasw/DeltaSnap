import pytest
import os

from tests.tools.db.database_connector import db_manajer
from tests.tools.test_db import setup_test_db

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
    db_manajer.drop_tables()
    db_manajer.create_tables()
    setup_test_db()
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


@pytest.fixture(scope='function')
def test_session():
    session = db_manajer.get_new_session()
    session.begin()
    yield session
    session.rollback()
    session.close()
