from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from typing import Type

from tests.tools.db.DBManajers.DBManajer import DBManager

class _Base(DeclarativeBase):
    pass

class SqlAlchemyDBManager(DBManager):
    def __init__(self):
        super().__init__()

    def _get_database_url(self):
        """Devuelve la URL para conectar con la base de datos de tipo SQLAlchemy."""
        match self.database:
            case "sqlite":
                return f"sqlite:///{self.db_path}"
            case "mysql":
                return f"mysql+mysqlconnector://{self.username}:{self.password}@localhost/{self.db_name}"
            case "postgresql":
                return f"postgresql://{self.username}:{self.password}@localhost/{self.db_name}"
            case _:
                raise Exception(f"Database {self.database} not supported")

    def _create_engine(self):
        """Devuelve el motor de SQLAlchemy."""
        return create_engine(self.db_path)

    def _create_sessionMaker(self):
        """Devuelve el sessionmaker de SQLAlchemy."""
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def _create_base(self):
        """Devuelve la clase Base de SQLAlchemy."""
        return _Base
    
    def get_base(self) -> Type[_Base]:
        """Devuelve la clase Base de SQLAlchemy."""
        return self.Base
    
    def get_newSession(self):
        """Devuelve una nueva sesión de SQLAlchemy."""
        return self.sessionMaker()

    def create_tables(self):
        """Crea las tablas en la base de datos."""
        self.Base.metadata.create_all(bind=self.engine)

    def drop_tables(self):
        """Elimina las tablas en la base de datos."""
        self.Base.metadata.drop_all(bind=self.engine)
