import os
from abc import ABC, abstractmethod

HOST = "localhost"
PORT = ''
PASSWORD = "test_password"
USERNAME = "test_user"
DATABASE = "mysql" # con sqlalchemy: sqlite | mysql | postgresql
DATABASE_NAME = "test_db"
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "test.db")

class DBManager(ABC):
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.database = DATABASE
        self.username = USERNAME
        self.password = PASSWORD
        self.db_name = DATABASE_NAME
        self.db_path = self._get_database_url()
    
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
    def get_base(self): ...
    
    @abstractmethod
    def get_newSession(self): ...

    @abstractmethod
    def create_tables(self) -> None: ...

    @abstractmethod
    def drop_tables(self) -> None: ...
