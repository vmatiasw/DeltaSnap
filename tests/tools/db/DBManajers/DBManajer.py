import os
from abc import ABC, abstractmethod

PASSWORD = "test_password"
USERNAME = "test_user"
DATABASE = "mysql" # con sqlalchemy: sqlite | mysql | postgresql
DATABASE_NAME = "test_db"
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "test.db")

class DBManager(ABC):
    def __init__(self):
        self.database = DATABASE
        self.username = USERNAME
        self.password = PASSWORD
        self.db_name = DATABASE_NAME
        self.db_path = self._get_database_url()
        self.engine = self._create_engine()
        self.sessionMaker = self._create_sessionMaker()
        self.Base = self._create_base()

    @abstractmethod
    def _get_database_url(self): ...

    @abstractmethod
    def _create_engine(self): ...

    @abstractmethod
    def _create_sessionMaker(self): ...
    
    @abstractmethod
    def _create_base(self): ...
    
    @abstractmethod
    def get_base(self): ...
    
    @abstractmethod
    def get_newSession(self): ...

    @abstractmethod
    def create_tables(self): ...

    @abstractmethod
    def drop_tables(self): ...
