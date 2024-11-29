from abc import ABC, abstractmethod
from typing import List, Any

from tests.tools.db.database_connector import db_connection_adapter as db_connection

class DBMetadataAdapter(ABC):
    def __init__(self) -> None:
        self.base = db_connection.get_base()
        
    @abstractmethod
    def get_tables(self) -> List: pass

    @staticmethod
    @abstractmethod
    def get_columns(table) -> List: pass

    @staticmethod
    @abstractmethod
    def get_instances(session, table, offset: int, page_size: int) -> List: pass
    
    @staticmethod
    @abstractmethod
    def get_column_key(column) -> str: pass
    
    @staticmethod
    @abstractmethod
    def get_column_value(columnKey, record) -> Any: pass
    
    @staticmethod
    @abstractmethod
    def column_is_foreign_key(column) -> bool: pass
    
    @staticmethod
    @abstractmethod
    def get_table_name(table) -> str: pass
    
    @staticmethod
    @abstractmethod
    def get_record_id(record) -> int: pass