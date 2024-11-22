import pytest

from DB.SqlAlchemyDB.db_setup import localSession

# Configurar logging para que muestre solo los errores
import logging
logging.getLogger().handlers.clear()  # Para evitar que se dupliquen los logs
logging.getLogger().level = logging.INFO
# Si se quiere ver los queries, cambiar a INFO
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)


@pytest.fixture(scope='function')
def test_db():
    db = localSession()
    yield db
    db.close()
