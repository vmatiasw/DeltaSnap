from typing import Any, Protocol, List


class IDBMetadata(Protocol):

    def get_tables(self) -> List[Any]:
        """Returns the tables or their mappers in the database."""
        ...

    def get_table_columns_from_table(self, table) -> List[Any]:
        """Returns the columns of a given table."""
        ...

    def get_table_columns_from_record(self, record) -> List[Any]:
        """Returns the columns of the table associated with the given record."""
        ...

    def get_records(self, table, offset: int, page_size: int) -> List[Any]:
        """Returns the records of the table within a specified range."""
        ...

    def get_column_name(self, column) -> str:
        """Returns the name of the column."""
        ...

    def get_field_value(self, column_name, record) -> Any:
        """Returns the value of the field in the record."""
        ...

    def column_is_foreign_key(self, column) -> bool:
        """Returns whether the column is a foreign key."""
        ...
        
    def column_is_relationship(self, column) -> bool:
        """Returns whether the column represents a relationship (e.g., OneToOne, ManyToOne)."""
        ...
        
    def get_record_by_field(self, column_name: str, record: Any) -> Any:
        """
        Returns the record that the foreign key points to.
        PRE: (column_name, record) is a foreign key.
        """
        ...

    def get_table_name_from_table(self, table) -> str:
        """Returns the name of the table."""
        ...

    def get_table_name_from_record(self, record) -> str:
        """Returns the name of the table associated with the record."""
        ...

    def get_record_id(self, record) -> int:
        """Returns the ID of the record."""
        ...

    def get_related_records(self, record) -> List[Any]:
        """Returns the related records of the given record."""
        ...

    def get_field_related_records(self, column_name, record) -> List[Any]:
        """Returns the related records for a specific field (column) in the record."""
        ...
