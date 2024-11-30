from typing import Any, List
from sqlalchemy.orm import Mapper, DeclarativeBase
from sqlalchemy import Column

from DeltaDB.DBMetadata.DBMetadataAdapter import DBMetadataAdapter

class SQLAlchemyMetadataAdapter(DBMetadataAdapter):
    def __init__(self, base: DeclarativeBase) -> None:
        super().__init__()
        self.base = base
    
    def get_tables(self) -> List[Mapper]:
        """Devuelve todos los mappers de las tablas en la base de datos."""
        return list(self.base.registry.mappers)
    
    def get_model_by_name(self, model_name: str) -> Any:
        """Obtiene un modelo de base de datos por su nombre."""
        for mapper in self.base.registry.mappers:
            if model_name == mapper.class_.__name__:
                return mapper.class_

        raise ValueError(f"El modelo {model_name} no se encuentra definido. \n modelos disponibles: {[mapper.class_.__name__ for mapper in self.base.registry.mappers]}")
    
    @staticmethod
    def get_columns(table: Any) -> List[Column]:
        """Devuelve las columnas de una tabla."""
        return list(table.columns)
    
    @staticmethod
    def get_instances(session: Any, table: Any, offset: int, page_size: int) -> List[Any]:
        """Devuelve las instancias de la tabla en un rango determinado."""
        return session.query(table.class_).limit(page_size).offset(offset).all()
    
    @staticmethod
    def get_column_key(column: Column) -> str:
        """Devuelve la clave de la columna."""
        return str(column.key)

    @staticmethod
    def get_column_value(column_key: str, record: Any) -> Any:
        """Devuelve el valor de una columna en un registro."""
        return getattr(record, column_key)
    
    @staticmethod
    def column_is_foreign_key(column: Column) -> bool:
        """Devuelve True si la columna es una clave foránea."""
        return bool(column.foreign_keys)
    
    @staticmethod
    def get_table_name(table: Any) -> str:
        """Devuelve el nombre de la tabla para el modelo dado."""
        return str(table.persist_selectable.name)
    
    @staticmethod
    def get_record_id(record: Any) -> int:
        """Devuelve el ID de un registro."""
        return int(record.id)
