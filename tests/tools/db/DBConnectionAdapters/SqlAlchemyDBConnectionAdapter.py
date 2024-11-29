from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase
from typing import Type

from tests.tools.db.DBConnectionAdapters.DBConnectionAdapter import DBConnectionAdapter

class _Base(DeclarativeBase):
    pass

class SqlAlchemyDBConnectionAdapter(DBConnectionAdapter):
    def __init__(self) -> None:
        super().__init__()
        self.engine: Engine = create_engine(self.db_path)
        self.sessionMaker: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base: Type[_Base] = _Base
    
    def get_base(self) -> Type[_Base]:
        """Devuelve la clase Base de SQLAlchemy."""
        return self.Base
    
    def get_new_session(self) -> Session:
        """Devuelve una nueva sesión de SQLAlchemy."""
        return self.sessionMaker()

    def create_tables(self) -> None:
        """Crea las tablas en la base de datos."""
        self.Base.metadata.create_all(bind=self.engine)

    def drop_tables(self) -> None:
        """Elimina las tablas en la base de datos."""
        self.Base.metadata.drop_all(bind=self.engine)
