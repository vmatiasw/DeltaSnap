from typing import Any, List
from django.db.models import Model, ForeignKey, ManyToOneRel, OneToOneRel, ManyToManyRel
from django.db.models.fields.related import ForeignObjectRel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.apps import apps
from django.db.models.manager import Manager
from django.db.models.fields.related import OneToOneField, ManyToManyField


class DjangoDBMetadata:
    def get_tables(self) -> List[type[Model]]:
        """Devuelve las tablas o modelos registrados en el proyecto."""
        return apps.get_models()

    def get_table_columns_from_table(self, table: type[Model]) -> List[Any]:
        """Devuelve las columnas de la tabla o modelo."""
        fields = table._meta.get_fields()
        return [field for field in fields] 

    def get_table_columns_from_record(self, record: Model) -> List[Model]:
        """Devuelve las columnas de la tabla asociada al registro."""
        return self.get_table_columns_from_table(record.__class__)

    def get_records(
        self, table: type[Model], offset: int, page_size: int
    ) -> List[Model]:
        """Devuelve los registros de la tabla en un rango determinado."""
        return list(table.objects.all()[offset : offset + page_size])

    def get_column_name(self, column: Any) -> str:
        """Devuelve el nombre de la columna."""
        return column.name

    def get_field_value(self, column_name: str, record: Model) -> Any:
        """Devuelve el valor de un campo en el registro."""
        return getattr(record, column_name, None)

    def column_is_foreign_key(self, column: Any) -> bool:
        """Devuelve si la columna es una clave foránea."""
        return isinstance(column, ForeignKey)

    def get_table_name_from_table(self, table: type[Model]) -> str:
        """Devuelve el nombre de la tabla asociada al modelo."""
        return table._meta.db_table

    def get_table_name_from_record(self, record: Model) -> str:
        """Devuelve el nombre de la tabla asociada al registro."""
        return self.get_table_name_from_table(record.__class__)

    def get_record_id(self, record: Model) -> int:
        """Devuelve el ID del registro."""
        return record.pk

    def get_related_records(self, record: Model) -> List[Model]:
        """Devuelve los registros relacionados con el registro dado."""
        related_objects = []

        for field in record._meta.get_fields():
            if not isinstance(
                field, (ForeignObjectRel, ManyToOneRel, OneToOneRel, ManyToManyRel)
            ):
                continue

            if isinstance(field, GenericForeignKey):
                continue

            accessor_name = field.get_accessor_name()
            if accessor_name:
                related_manager = getattr(record, accessor_name, None)

                if related_manager and hasattr(related_manager, "all"):
                    related_objects.extend(related_manager.all())

        return related_objects

    def get_record_by_field(self, column_name: str, record: Model) -> Model:
        """
        Devuelve el registro al que apunta la clave foránea.
        PRE: field (column_name, record) es una clave foránea.
        """
        return getattr(record, column_name)

    def column_is_relationship(self, column) -> bool:
        """
        Devuelve si la columna es una relación no clave foranea (OneToOne, ManyToOne o ManyToMany).
        """
        algo = isinstance(column, (OneToOneField, ManyToManyField))
        algo2 = issubclass(
            column.__class__,
            (ForeignObjectRel, ManyToOneRel, OneToOneRel, ManyToManyRel),
        )
        return algo or algo2

    def get_field_related_records(
        self, column_name: str, record: Model
    ) -> List[Manager]:
        """
        Devuelve los registros relacionados para una columna de tipo relación.
        PRE: La columna debe ser una relación.
        """
        column = next(
            (field for field in record._meta.get_fields() if field.name == column_name),
            None,
        )

        if not column or not self.column_is_relationship(column):
            return []

        related_manager: Manager = getattr(record, column_name, None)

        if hasattr(related_manager, "all"):
            return list(related_manager.all())

        if related_manager:
            return [related_manager]

        return []
