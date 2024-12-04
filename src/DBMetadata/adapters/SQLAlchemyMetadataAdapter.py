from typing import Any, Protocol, List, Type, runtime_checkable

from sqlalchemy.orm import Mapper, DeclarativeBase, Query
from sqlalchemy import Column, Table


@runtime_checkable
class IRepository(Protocol):

    def query(self, model: Type[Any]) -> Query: ...


class SQLAlchemyMetadataAdapter:
    def __init__(self, base: DeclarativeBase, repository: IRepository) -> None:
        super().__init__()
        self.base = base
        self.repository = repository

    def get_tables(self) -> List[Mapper]:
        """Devuelve todos los mappers de las tablas en la base de datos."""
        return list(self.base.registry.mappers)

    @staticmethod
    def get_table_columns_from_table(table: Mapper) -> List[Column]:
        """Devuelve las columnas de una tabla."""
        return list(table.columns)

    def get_table_columns_from_record(self, record: Any) -> List[Column]:
        """Devuelve las columnas de un registro."""
        return self.get_table_columns_from_table(record.__mapper__.persist_selectable)

    def get_records(self, table: Mapper, offset: int, page_size: int) -> List[Any]:
        """Devuelve las instancias de la tabla en un rango determinado."""
        return self.repository.query(table.class_).limit(page_size).offset(offset).all()

    @staticmethod
    def get_column_name(column: Column) -> str:
        """Devuelve la clave de la columna."""
        return str(column.key)

    @staticmethod
    def get_column_value(column_name: str, record: Any) -> Any:
        """Devuelve el valor de una columna en un registro."""
        return getattr(record, column_name)

    @staticmethod
    def column_is_foreign_key(column: Column) -> bool:
        """Devuelve True si la columna es una clave foránea."""
        return bool(column.foreign_keys)

    @staticmethod
    def get_table_name_from_table(table: Mapper) -> str:
        """Devuelve el nombre de la tabla para el modelo dado."""
        real_table : Table = table.persist_selectable
        return real_table.name

    @staticmethod
    def get_table_name_from_record(record: Any) -> str:
        """Devuelve el nombre de la tabla para un registro."""
        return record.__mapper__.persist_selectable.name

    @staticmethod
    def get_record_id(record: Any) -> int:
        """Devuelve el ID de un registro."""
        return int(record.id)
