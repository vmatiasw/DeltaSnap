from typing import Any, List
from django.db import models
from django.apps import apps

from DeltaDB.DBMetadata.DBMetadataAdapter import DBMetadataAdapter

class DjangoMetadataAdapter(DBMetadataAdapter):
    def __init__(self) -> None:
        super().__init__()

    def get_tables(self) -> List[type[models.Model]]:
        """Devuelve todas las clases de modelo registradas en Django."""
        return list(apps.get_models())

    @staticmethod
    def get_columns(table) -> List[models.Field]:
        """Devuelve los campos de un modelo (tabla) específico."""
        return list(table._meta.fields)
    
    @staticmethod
    def get_instances(session, table, offset: int, page_size: int) -> List:
        """Devuelve los registros de una tabla en un rango determinado."""
        queryset = table.objects.all()
        return list(queryset[offset:offset + page_size])

    @staticmethod
    def get_column_key(column) -> str:
        """Devuelve el nombre del campo (columna) del modelo."""
        return str(column.name)
    
    @staticmethod
    def get_column_value(column_key, record) -> Any:
        """Devuelve el valor del campo (columna) para un registro dado."""
        return getattr(record, column_key)
    
    @staticmethod
    def column_is_foreign_key(column) -> bool:
        """Devuelve True si el campo es una clave foránea, False de lo contrario."""
        return isinstance(column, models.ForeignKey)
    
    @staticmethod
    def get_table_name(table) -> str:
        """Devuelve el nombre de la tabla asociada al modelo."""
        return str(table._meta.db_table)
    
    @staticmethod
    def get_record_id(record) -> int:
        """Devuelve el ID del registro (específicamente en Django, es el campo de la clave primaria)."""
        return int(record.id)
