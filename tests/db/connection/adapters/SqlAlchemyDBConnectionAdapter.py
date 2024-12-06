from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Type

from tests.db.connection.IDBConnection import IDBConnection
from tests.db.models.sql_alchemy import Base


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

    def get_new_session(self) -> Session:
        """Devuelve una nueva sesión de SQLAlchemy."""
        return self.sessionMaker()

    def create_tables(self) -> None:
        """Crea las tablas en la base de datos."""
        self.base.metadata.create_all(bind=self.engine)

    def drop_tables(self) -> None:
        """Elimina las tablas en la base de datos."""
        self.base.metadata.drop_all(bind=self.engine)
