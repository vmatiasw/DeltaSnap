import pytest
import os
import logging

from DeltaDB import DBCapturer, DBConfig

from tests.db.DBContextManager import DBTestContextManager
from tests.db.GameFactory import GameFactory
from tests.db.repository.manager import get_repository
from tests.db.connection.manager import get_db_connection
from tests.db.TestDB import TestDB
from tests.db.config import DB_PATH

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture(scope="function", autouse=True)
def db_connection(db_source):
    yield get_db_connection(db_source)


@pytest.fixture(scope="function", autouse=True)
def setup_db(db_connection):
    if os.path.exists(DB_PATH):
        logging.info(f"DB {DB_PATH} already exists")
        return

    try:
        with DBTestContextManager(db_connection.get_new_session()):
            db_connection.drop_tables()
            db_connection.create_tables()
            TestDB(get_repository(db_connection)).setup_data()
            yield
    finally:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)


@pytest.fixture(scope="function", autouse=True)
def db_session(db_connection, setup_db):
    with DBTestContextManager(db_connection.get_new_session()):
        yield


@pytest.fixture(scope="function")
def repository(db_connection, db_session):
    yield get_repository(db_connection)


@pytest.fixture(scope="function")
def game(repository):
    yield GameFactory(repository)


@pytest.fixture(scope="function")
def db_capturer(db_connection, repository):
    yield DBCapturer(
        DBConfig(
            db_source=db_connection.db_source,
            test_session=repository.get_current_session(),
            base=db_connection.get_base(),
        )
    )
