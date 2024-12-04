from collections import defaultdict
from typing import Any, List, Dict

from DeltaDB.domain.types import Capture
from DeltaDB.domain.interfaces.IDBMetadata import IDBMetadata


def capture_related_records(db_metadata: IDBMetadata, records: List[Any]) -> Capture:
    """
    Captures the structure and data of the specified records and their related records.

    Args:
        records (object): The records to be captured.

    Returns:
        object: The result of the capture processed by the adapter.
    """
    capture: Capture = defaultdict(dict)
    stack = []

    for record in records:
        stack.append(record)

    while stack:
        record = stack.pop()
        table_name = db_metadata.get_table_name_from_record(record)
        record_id = db_metadata.get_record_id(record)

        if capture.get((table_name, record_id)):
            continue

        columns = db_metadata.get_table_columns_from_record(record)
        capture[table_name, record_id] = __extract_fields_values(
            db_metadata, record, columns
        )

        related_records = db_metadata.get_related_records(record)
        for related_record in related_records:
            stack.append(related_record)

    return dict(capture)


def capture_records(db_metadata: IDBMetadata, records: List[Any]) -> Capture:
    """
    Captures the structure and data of the specified records.

    Args:
        records (object): The records to be captured.

    Returns:
        object: The result of the capture processed by the adapter.
    """
    capture: Capture = defaultdict(dict)

    for record in records:
        table_name = db_metadata.get_table_name_from_record(record)
        record_id = db_metadata.get_record_id(record)
        columns = db_metadata.get_table_columns_from_record(record)
        capture[table_name, record_id] = __extract_fields_values(
            db_metadata, record, columns
        )

    return dict(capture)


def capture_all_records(db_metadata: IDBMetadata, page_size: int = 1000) -> Capture:
    """
    Captures the structure and data of all tables in the database.

    Args:
        page_size (int): The number of records to capture per page.

    Returns:
        object: The result of the capture processed by the adapter.
    """
    tables = db_metadata.get_tables()
    capture: Capture = defaultdict(dict)

    for table in tables:
        offset = 0
        columns = db_metadata.get_table_columns_from_table(table)
        table_name = db_metadata.get_table_name_from_table(table)

        while records := db_metadata.get_records(table, offset, page_size):

            for record in records:
                record_id = db_metadata.get_record_id(record)
                capture[table_name, record_id] = __extract_fields_values(
                    db_metadata, record, columns
                )

            offset += page_size

    return dict(capture)


def __extract_fields_values(
    db_metadata: IDBMetadata, record: Any, fields: List[Any]
) -> Dict[str, Any]:
    fields_values: Dict[str, Any] = defaultdict(dict)

    for field in fields:
        column_name = db_metadata.get_column_name(field)
        field_value = db_metadata.get_field_value(column_name, record)
        column_is_foreign_key = db_metadata.column_is_foreign_key(field)
        key = f"{column_name} (FK)" if column_is_foreign_key else column_name
        fields_values[key] = field_value

    return dict(fields_values)
