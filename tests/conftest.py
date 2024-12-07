import pytest
import os
import logging

from DeltaDB import DBCapturer, DBConfig

from tests.db.DBContextManager import DBTestContextManager
from tests.db.game_test.GameFactory import GameFactory
from tests.db.repository.manager import get_repository
from tests.db.connection.manager import get_db_connection
from tests.db.game_test.setup_db_data import setup_db_data
from tests.db.config import DB_PATH, DB_SOURCES

logging.basicConfig(level=logging.DEBUG)


# ---------------------------- SESSION FIXTURES ----------------------------


@pytest.fixture(scope="session", params=DB_SOURCES)
def db_connection(request):
    yield get_db_connection(request.param)


@pytest.fixture(scope="session")
def repository(db_connection):
    yield get_repository(db_connection)


@pytest.fixture(scope="session")
def game(repository):
    yield GameFactory(repository)


@pytest.fixture(scope="session", autouse=True)
def setup_db(db_connection, game, repository):
    if os.path.exists(DB_PATH):
        logging.info(f"DB {DB_PATH} already exists")
        return

    try:
        with DBTestContextManager(db_connection.get_new_session()):
            db_connection.drop_tables()
            db_connection.create_tables()
            setup_db_data(repository, game)
            yield
    finally:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)


# ---------------------------- FUNCTION FIXTURES ----------------------------


@pytest.fixture(scope="function")
def db_session(db_connection):
    session = db_connection.get_new_session()
    with DBTestContextManager(session):
        yield session


@pytest.fixture(scope="function")
def db_capturer(db_connection, db_session):
    yield DBCapturer(
        DBConfig(
            db_source=db_connection.db_source,
            test_session=db_session,
            base=db_connection.get_base(),
        )
    )
