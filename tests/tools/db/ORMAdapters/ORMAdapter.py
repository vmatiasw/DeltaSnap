from abc import ABC, abstractmethod
from typing import List, Any

from tests.tools.db.database_connector import db_manajer

class ORMAdapter(ABC):
    def __init__(self) -> None:
        self.base = db_manajer.get_base()
        
    @abstractmethod
    def get_tables(self) -> List: ...

    @staticmethod
    @abstractmethod
    def get_columns(table) -> List: ...

    @staticmethod
    @abstractmethod
    def get_instances(session, table, offset: int, page_size: int) -> List: ...
    
    @staticmethod
    @abstractmethod
    def get_column_key(column) -> str: ...
    
    @staticmethod
    @abstractmethod
    def get_column_value(columnKey, record) -> Any: ...
    
    @staticmethod
    @abstractmethod
    def column_is_foreign_key(column) -> bool: ...
    
    @staticmethod
    @abstractmethod
    def get_table_name(table) -> str: ...
    
    @staticmethod
    @abstractmethod
    def get_record_id(record) -> int: ...