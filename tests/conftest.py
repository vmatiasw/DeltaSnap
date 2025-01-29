import pytest
import os
import logging

from src.deltasnap import DBCapturer, DBConfig

from tests.db.connection.IDBConnection import IDBConnection
from tests.db.repository.IRepository import IRepository
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
def repository(db_connection: IDBConnection):
    yield get_repository(db_connection)


@pytest.fixture(scope="session")
def game(repository: IRepository):
    yield GameFactory(repository)


@pytest.fixture(scope="session", autouse=True)
def setup_db(db_connection: IDBConnection, game: GameFactory, repository: IRepository):
    if os.path.exists(DB_PATH):
        logging.info(f"DB {DB_PATH} already exists")
        yield

    try:
        db_connection.drop_tables()
        db_connection.create_tables()
        with db_connection.new_test_transaction():
            setup_db_data(repository, game)
            yield
    finally:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)


# ---------------------------- FUNCTION FIXTURES ----------------------------


@pytest.fixture(scope="function")
def db_session(db_connection: IDBConnection):
    with db_connection.new_test_transaction() as session:
        yield session


@pytest.fixture(scope="function")
def db_capturer(db_connection: IDBConnection, db_session):
    yield DBCapturer(
        DBConfig(
            db_source=db_connection.db_source,
            test_session=db_session,
            base=db_connection.get_base(),
        )
    )


@pytest.fixture(scope="function")
def differences(repository: IRepository, db_capturer: DBCapturer, game: GameFactory):
    captura_inicial = db_capturer.capture_all_records()
    game.start_game(repository.get("Game", 1))
    captura_final = db_capturer.capture_all_records()

    captura_inicial[("players", 1)].pop("is_creator")
    captura_final[("players", 1)].pop("name")

    return DBCapturer.compare_capture(captura_inicial, captura_final)
