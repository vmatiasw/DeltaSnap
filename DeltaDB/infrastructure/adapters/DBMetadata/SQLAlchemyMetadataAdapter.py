from typing import Any, List

from sqlalchemy.orm import Mapper, DeclarativeBase, Session, RelationshipProperty
from sqlalchemy import Column, Table, inspect


class SQLAlchemyMetadataAdapter:
    def __init__(self, base: DeclarativeBase, test_session: Session) -> None:
        super().__init__()
        self.base = base
        self.test_session = test_session

    def get_tables(self) -> List[Mapper]:
        """Devuelve todos los mappers de las tablas en la base de datos."""
        return list(self.base.registry.mappers)

    def get_table_columns_from_table(self, table: Mapper) -> List[Column | RelationshipProperty]:
        """
        Devuelve las columnas de una tabla, evitando agregar relaciones redundantes
        si ya existe una clave foránea asociada a la relación.
        """
        columns: List[Column | RelationshipProperty] = list(table.columns)

        existing_foreign_keys = {
            (fk.column.table.name, fk.parent.key) 
            for col in table.columns if hasattr(col, 'foreign_keys') for fk in col.foreign_keys
        }

        for rel_name, rel in table.relationships.items():
            if isinstance(rel, RelationshipProperty):
                rel_id = (self.get_table_name_from_table(rel.mapper), list(rel.local_columns)[0].key)
                if not rel_id in existing_foreign_keys:
                    columns.append(rel)

        return columns

    def get_table_columns_from_record(self, record: Any) -> List[Column|RelationshipProperty]:
        """Devuelve las columnas de un registro."""
        mapper: Mapper = record.__mapper__
        return self.get_table_columns_from_table(mapper)

    def get_records(self, table: Mapper, offset: int, page_size: int) -> List[Any]:
        """Devuelve las instancias de la tabla en un rango determinado."""
        return (
            self.test_session.query(table.class_).limit(page_size).offset(offset).all()
        )

    @staticmethod
    def get_column_name(column: Column|RelationshipProperty) -> str:
        """Devuelve la clave de la columna."""
        return str(column.key)

    @staticmethod
    def get_field_value(column_name: str, record: Any) -> Any:
        """Devuelve el valor de una columna en un registro."""
        return getattr(record, column_name)

    @staticmethod
    def column_is_foreign_key(column: Column|RelationshipProperty) -> bool:
        """Devuelve True si la columna es una clave foránea."""
        return not isinstance(column, RelationshipProperty) and bool(column.foreign_keys)

    @staticmethod
    def column_is_relationship(column: Column|RelationshipProperty) -> bool:
        """Devuelve True si la columna es una ralacion."""
        return isinstance(column, RelationshipProperty)

    @staticmethod
    def get_table_name_from_table(table: Mapper) -> str:
        """Devuelve el nombre de la tabla para el modelo dado."""
        real_table: Table = table.persist_selectable
        return real_table.name

    @staticmethod
    def get_table_name_from_record(record: Any) -> str:
        """Devuelve el nombre de la tabla para un registro."""
        return record.__mapper__.persist_selectable.name

    @staticmethod
    def get_record_id(record: Any) -> int:
        """Devuelve el ID de un registro."""
        return int(record.id)

    @staticmethod
    def get_related_records(record: Any) -> List[Any]:
        """
        Dado un registro, obtiene todos los registros relacionados a través de sus relaciones.

        :param record: El registro del cual obtener las relaciones.
        :return: Una lista con los registros relacionados.
        """
        related_records = []
        relationships = inspect(record.__class__).relationships
        
        for rel_name, rel in relationships.items():
            related_data = getattr(record, rel_name)
            if isinstance(related_data, list):
                related_records.extend(related_data)
            elif related_data is not None:
                related_records.append(related_data)

        return related_records
    
    def get_field_related_records(self, column_name, record) -> List[Any]:
        """Devuelve los registros relacionados de la columna"""
        related_records = []
        relationships = inspect(record.__class__).relationships

        for rel_name, rel in relationships.items():
            if rel_name == column_name:
                related_data = getattr(record, rel_name)
                if isinstance(related_data, list):
                    related_records.extend(related_data)
                elif related_data is not None:
                    related_records.append(related_data)

        return related_records
        
    
    def get_record_by_field(self, column_name: str, record: Any):
        """
        Devuelve el registro al que apunta la clave foránea.
        PRE: field (column_name, record) es una clave foránea.
        """
        column_value = getattr(record, column_name)
        relationships = inspect(record.__class__).relationships

        for rel_name, rel in relationships.items():
            related_data = getattr(record, rel_name)
            
            if isinstance(related_data, list):
                for related_record in related_data:
                    if related_record.id == column_value:
                        return related_record 
            elif related_data and related_data.id == column_value:
                return related_data