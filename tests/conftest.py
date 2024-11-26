import pytest
import os

from tests.tools.db.db_setup import localSession

# Configurar logging para que muestre solo los errores
import logging
logging.getLogger().handlers.clear()  # Para evitar que se dupliquen los logs
logging.getLogger().level = logging.INFO
# Si se quiere ver los queries, cambiar a INFO
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

DB_PATH = os.path.join('tests/tools/db/test.db')


@pytest.fixture(scope='session', autouse=True)
def setup_db():
    if not os.path.exists(DB_PATH):
        from tests.tools.db.db_setup import Base, engine
        from tests.tools.test_db import setup_test_db
        Base.metadata.create_all(engine)
        setup_test_db()
        os.chmod(DB_PATH, 0o444)  # Permisos de solo lectura (r-- r-- r--)
    yield


@pytest.fixture(scope='function')
def test_session():
    os.chmod(DB_PATH, 0o644)  # Volver a permisos de escritura (rw- rw- rw-)
    session = localSession()
    session.begin()
    yield session
    session.rollback()
    session.close()
    os.chmod(DB_PATH, 0o444)  # Permisos de solo lectura (r-- r-- r--)
