from typing import Any, List
from sqlalchemy.orm import Mapper, DeclarativeBase, Session, RelationshipProperty
from sqlalchemy import Column, Table, inspect


class SQLAlchemyMetadataAdapter:
    def __init__(self, base: DeclarativeBase, test_session: Session) -> None:
        super().__init__()
        self.base = base
        self.test_session = test_session

    def get_tables(self) -> List[Mapper]:
        """Returns all table mappers in the database."""
        return list(self.base.registry.mappers)

    def get_table_columns_from_table(
        self, table: Mapper
    ) -> List[Column | RelationshipProperty]:
        """
        Returns the columns of a table, avoiding redundant relationships
        if a foreign key is already associated with the relationship.
        """
        columns: List[Column | RelationshipProperty] = list(table.columns)

        existing_foreign_keys = {
            (fk.column.table.name, fk.parent.key)
            for col in table.columns
            if hasattr(col, "foreign_keys")
            for fk in col.foreign_keys
        }

        for rel_name, rel in table.relationships.items():
            if isinstance(rel, RelationshipProperty):
                rel_id = (
                    self.get_table_name_from_table(rel.mapper),
                    list(rel.local_columns)[0].key,
                )
                if not rel_id in existing_foreign_keys:
                    columns.append(rel)

        return columns

    def get_table_columns_from_record(
        self, record: Any
    ) -> List[Column | RelationshipProperty]:
        """Returns the columns of a record."""
        mapper: Mapper = record.__mapper__
        return self.get_table_columns_from_table(mapper)

    def get_records(self, table: Mapper, offset: int, page_size: int) -> List[Any]:
        """Returns the instances of the table within a given range."""
        return (
            self.test_session.query(table.class_).limit(page_size).offset(offset).all()
        )

    @staticmethod
    def get_column_name(column: Column | RelationshipProperty) -> str:
        """Returns the column key."""
        return str(column.key)

    @staticmethod
    def get_field_value(column_name: str, record: Any) -> Any:
        """Returns the value of a column in a record."""
        return getattr(record, column_name)

    @staticmethod
    def column_is_foreign_key(column: Column | RelationshipProperty) -> bool:
        """Returns True if the column is a foreign key."""
        return not isinstance(column, RelationshipProperty) and bool(
            column.foreign_keys
        )

    @staticmethod
    def column_is_relationship(column: Column | RelationshipProperty) -> bool:
        """Returns True if the column is a relationship."""
        return isinstance(column, RelationshipProperty)

    @staticmethod
    def get_table_name_from_table(table: Mapper) -> str:
        """Returns the table name for the given model."""
        real_table: Table = table.persist_selectable
        return real_table.name

    @staticmethod
    def get_table_name_from_record(record: Any) -> str:
        """Returns the table name for a record."""
        return record.__mapper__.persist_selectable.name

    @staticmethod
    def get_record_id(record: Any) -> int:
        """Returns the ID of a record."""
        return int(record.id)

    @staticmethod
    def get_related_records(record: Any) -> List[Any]:
        """
        Given a record, retrieves all records related through its relationships.

        :param record: The record from which to get the relationships.
        :return: A list of related records.
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
        """Returns the related records of the column."""
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
        Returns the record that a foreign key points to.
        PRE: field (column_name, record) is a foreign key.
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
