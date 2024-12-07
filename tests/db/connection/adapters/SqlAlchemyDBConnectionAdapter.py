from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Type, Generator, Any
from contextlib import contextmanager
from contextvars import ContextVar, Token

from tests.db.connection.IDBConnection import IDBConnection
from tests.db.game_test.models.sql_alchemy import Base


current_session: ContextVar[Session] = ContextVar("current_session")


class SqlAlchemyDBConnectionAdapter(IDBConnection):
    def __init__(self, db_source) -> None:
        super().__init__()
        self.db_source: str = db_source
        self.engine: Engine = create_engine(self.db_path)
        self.sessionMaker: sessionmaker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self.base: Type[Base] = Base

    def get_base(self) -> Type[Base]:
        """Devuelve la clase Base de SQLAlchemy."""
        return self.base

    @contextmanager
    def new_transaction(self) -> Generator[Any, Any, Any]:
        """
        Un administrador de contexto para manejar transacciones en modo de prueba.

        Args:
            session (Any): Sesión de la base de datos a gestionar en el contexto.

        Yields:
            session (Any): La sesión gestionada para el contexto.
        """
        session: Session = self.sessionMaker()
        token = current_session.set(session)
        try:
            session.begin()
            yield session
        except Exception as e:
            raise
        finally:
            try:
                session.rollback()
            finally:
                session.close()
                current_session.reset(token)

    def create_tables(self) -> None:
        """Crea las tablas en la base de datos."""
        self.base.metadata.create_all(bind=self.engine)

    def drop_tables(self) -> None:
        """Elimina las tablas en la base de datos."""
        self.base.metadata.drop_all(bind=self.engine)
