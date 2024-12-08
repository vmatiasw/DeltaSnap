from typing import Any, Protocol, List


class IDBMetadata(Protocol):

    def get_tables(self) -> List[Any]:
        """Devuelve las tablas o sus mappers en la base de datos."""
        ...

    def get_table_columns_from_table(self, table) -> List[Any]:
        """Devuelve las columnas de la tabla."""
        ...

    def get_table_columns_from_record(self, record) -> List[Any]:
        """Devuelve las columnas de la tabla del registro."""
        ...

    def get_records(self, table, offset: int, page_size: int) -> List[Any]:
        """Devuelve los registros de la tabla en un rango determinado."""
        ...

    def get_column_name(self, column) -> str:
        """Devuelve el nombre de la columna."""
        ...

    def get_field_value(self, column_name, record) -> Any:
        """Devuelve el valor del campo en el registro"""
        ...

    def column_is_foreign_key(self, column) -> bool:
        """Devuelve si la columna es una clave foranea"""
        ...
        
    def column_is_relationship(self, column) -> bool:
        """Devuelve si la columna es una relacion"""
        ...
        
    def get_record_by_field(self, column_name: str, record: Any) -> Any:
        """
        Devuelve el registro al que apunta la clave foránea.
        PRE: field (column_name, record) es una clave foránea.
        """
        ...

    def get_table_name_from_table(self, table) -> str:
        """Devuelve el nombre de la tabla"""
        ...

    def get_table_name_from_record(self, record) -> str:
        """Devuelve el nombre de la tabla del registro"""
        ...

    def get_record_id(self, record) -> int:
        """Devuelve el id del registro"""
        ...

    def get_related_records(self, record) -> List[Any]:
        """Devuelve los registros relacionados"""
        ...

    def get_field_related_records(self, column_name, record) -> List[Any]:
        """Devuelve los registros relacionados de la columna"""
        ...