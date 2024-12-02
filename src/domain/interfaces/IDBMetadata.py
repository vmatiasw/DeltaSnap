from typing import Any, Protocol, List


class IDBMetadata(Protocol):

    def get_tables(self) -> List: pass

    def get_columns(self, table) -> List: pass

    def get_instances(self, table, offset: int, page_size: int) -> List: pass

    def get_column_key(self, column) -> str: pass

    def get_column_value(self, columnKey, record) -> Any: pass

    def column_is_foreign_key(self, column) -> bool: pass

    def get_table_name(self, table) -> str: pass

    def get_record_id(self, record) -> int: pass
