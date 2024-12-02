import os
from abc import ABC, abstractmethod

from tests.db.config import DATABASE, DATABASE_NAME, HOST, PASSWORD, PORT, USERNAME

DATABASE_PATH = os.path.join(os.path.dirname(__file__), f"{DATABASE_NAME}.db")

class IDBConnection(ABC):
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.database = DATABASE
        self.username = USERNAME
        self.password = PASSWORD
        self.db_name = DATABASE_NAME
        self.db_path = self._get_database_url()
        self.base = None
    
    @staticmethod
    def _get_database_url() -> str:
        """Devuelve la URL para conectar con la base de datos."""
        port = f":{PORT}" if PORT else ""
        match DATABASE:
            case "sqlite":
                return f"sqlite:///{DATABASE_PATH}"
            case "mysql":
                return f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}{port}/{DATABASE_NAME}"
            case "postgresql":
                return f"postgresql://{USERNAME}:{PASSWORD}@{HOST}{port}/{DATABASE_NAME}"
            case _:
                raise Exception(f"Database {DATABASE} not supported")
    
    @abstractmethod
    def get_base(self): pass
    
    @abstractmethod
    def get_new_session(self): pass

    @abstractmethod
    def create_tables(self) -> None: pass

    @abstractmethod
    def drop_tables(self) -> None: pass
