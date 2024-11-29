
from typing import Any, List

from tests.tools.db.ORMAdapters.ORMAdapter import ORMAdapter

class SQLAlchemyAdapter(ORMAdapter):
    def __init__(self):
        super().__init__()
    
    def get_tables(self) -> List:
        return self.base.registry.mappers
    
    @staticmethod
    def get_columns(table) -> List:
        return table.columns
    
    @staticmethod
    def get_instances(session, table, offset: int, page_size: int) -> List:
        return session.query(table.class_).limit(page_size).offset(offset).all()
    
    @staticmethod
    def get_column_key(column) -> str:
        return column.key 
    
    @staticmethod
    def get_column_value(column_key, record) -> Any:
        return getattr(record, column_key)
    
    @staticmethod
    def column_is_foreign_key(column) -> bool:
        return bool(column.foreign_keys)
    
    @staticmethod
    def get_table_name(table) -> str:
        return str(table.persist_selectable.name)
    
    @staticmethod
    def get_record_id(record) -> int:
        return record.id
        