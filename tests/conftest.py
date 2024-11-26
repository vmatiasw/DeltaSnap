import pytest

from tests.tools.DB.db_setup import localSession

# Configurar logging para que muestre solo los errores
import logging
logging.getLogger().handlers.clear()  # Para evitar que se dupliquen los logs
logging.getLogger().level = logging.INFO
# Si se quiere ver los queries, cambiar a INFO
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)

@pytest.fixture(scope='session', autouse=True)
def setup_db():
    from tests.tools.DB.db_setup import Base, engine
    from tests.tools.test_db import setup_test_db
    Base.metadata.create_all(engine)
    setup_test_db()
    yield

@pytest.fixture(scope='function')
def test_session():
    session = localSession()
    session.begin()
    yield session
    session.rollback()
    session.close()
