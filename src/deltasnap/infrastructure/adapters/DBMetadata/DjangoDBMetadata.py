from typing import Any, List
from django.db.models import Model, ForeignKey, ManyToOneRel, OneToOneRel, ManyToManyRel
from django.db.models.fields.related import ForeignObjectRel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.apps import apps
from django.db.models.manager import Manager
from django.db.models.fields.related import OneToOneField, ManyToManyField


class DjangoDBMetadata:
    def get_tables(self) -> List[type[Model]]:
        """Returns all the models (tables) registered in the project."""
        return apps.get_models()

    def get_table_columns_from_table(self, table: type[Model]) -> List[Any]:
        """Returns the columns of the table (model)."""
        fields = table._meta.get_fields()
        return [field for field in fields]

    def get_table_columns_from_record(self, record: Model) -> List[Model]:
        """Returns the columns of the table associated with the given record."""
        return self.get_table_columns_from_table(record.__class__)

    def get_records(
        self, table: type[Model], offset: int, page_size: int
    ) -> List[Model]:
        """Returns records from the table within a specified range."""
        return list(table.objects.all()[offset : offset + page_size])

    def get_column_name(self, column: Any) -> str:
        """Returns the column name."""
        return column.name

    def get_field_value(self, column_name: str, record: Model) -> Any:
        """Returns the value of a field in the given record."""
        return getattr(record, column_name, None)

    def column_is_foreign_key(self, column: Any) -> bool:
        """Returns True if the column is a foreign key."""
        return isinstance(column, ForeignKey)

    def get_table_name_from_table(self, table: type[Model]) -> str:
        """Returns the table name associated with the model."""
        return table._meta.db_table

    def get_table_name_from_record(self, record: Model) -> str:
        """Returns the table name associated with the given record."""
        return self.get_table_name_from_table(record.__class__)

    def get_record_id(self, record: Model) -> int:
        """Returns the ID of the record."""
        return record.pk

    def get_related_records(self, record: Model) -> List[Model]:
        """
        Returns all records related to the given record through its relationships.
        """
        related_objects = []

        for field in record._meta.get_fields():
            # Skip non-relationship fields
            if not isinstance(
                field, (ForeignObjectRel, ManyToOneRel, OneToOneRel, ManyToManyRel)
            ):
                continue

            # Skip generic foreign keys
            if isinstance(field, GenericForeignKey):
                continue

            # Get the related objects via the accessor name
            accessor_name = field.get_accessor_name()
            if accessor_name:
                related_manager = getattr(record, accessor_name, None)

                # Ensure the related manager has the 'all' method to fetch related records
                if related_manager and hasattr(related_manager, "all"):
                    related_objects.extend(related_manager.all())

        return related_objects

    def get_record_by_field(self, column_name: str, record: Model) -> Model:
        """
        Returns the record that a foreign key points to.
        PRE: The column (column_name, record) should be a foreign key.
        """
        return getattr(record, column_name)

    def column_is_relationship(self, column) -> bool:
        """
        Returns True if the column is a relationship (not a foreign key).
        Relationships include OneToOne, ManyToOne, or ManyToMany.
        """
        is_relationship_field = isinstance(column, (OneToOneField, ManyToManyField))
        is_relationship_class = issubclass(
            column.__class__,
            (ForeignObjectRel, ManyToOneRel, OneToOneRel, ManyToManyRel),
        )
        return is_relationship_field or is_relationship_class

    def get_field_related_records(
        self, column_name: str, record: Model
    ) -> List[Manager]:
        """
        Returns the related records for a relationship field.
        PRE: The column should be a relationship field.
        """
        column = next(
            (field for field in record._meta.get_fields() if field.name == column_name),
            None,
        )

        # If no relationship column is found or it's not a relationship type, return an empty list
        if not column or not self.column_is_relationship(column):
            return []

        related_manager: Manager = getattr(record, column_name, None)

        # Return the related records, handling both "all" relationships and singular relationships
        if hasattr(related_manager, "all"):
            return list(related_manager.all())

        if related_manager:
            return [related_manager]

        return []
