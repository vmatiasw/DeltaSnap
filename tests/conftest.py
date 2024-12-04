import DeltaDB
import pytest
import os

from tests.db.DBContextManager import DBTestContextManager
from tests.db.GameFactory import GameFactory
from tests.db.repository.manajer import Repository
from tests.db.connection.manajer import DBConnection
from tests.db.TestDB import TestDB
from tests.db.config import DATABASE_NAME

# Configurar logging para que muestre solo los errores
import logging

logging.getLogger().handlers.clear()  # Para evitar que se dupliquen los logs
logging.getLogger().level = logging.INFO
# Si se quiere ver los queries, cambiar a INFO
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

DB_PATH = os.path.join(f"tests/db/connection/{DATABASE_NAME}.db")


@pytest.fixture(scope="session", autouse=True)
def setup_db(db_connection):
    if os.path.exists(DB_PATH):
        logging.info(f"DB {DB_PATH} already exists")
        return

    try:
        with DBTestContextManager(db_connection.get_new_session()):
            db_connection.drop_tables()
            db_connection.create_tables()
            TestDB(Repository(base=db_connection.get_base())).setup_data()
            yield
    finally:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)


@pytest.fixture(scope="session")
def db_connection():
    yield DBConnection()


@pytest.fixture(scope="function")
def repository(db_connection):
    with DBTestContextManager(db_connection.get_new_session()):
        yield Repository(base=db_connection.get_base())


@pytest.fixture(scope="function")
def game(repository):
    yield GameFactory(repository)


@pytest.fixture(scope="function")
def delta_db(repository, db_connection):
    yield DeltaDB.DeltaDB(
        db_type="sqlite",
        db_orm="sqlalchemy",
        repository=repository,
        base=db_connection.get_base(),
    )
