from collections import defaultdict
from typing import Any, List, Dict

from src.domain.types import Capture
from src.domain.interfaces.IDBMetadata import IDBMetadata


def capture_related_records(db_metadata: IDBMetadata, records: List[Any]) -> Capture:
    """Captura iterativamente los registros relacionados a los registros proporcionados utilizando una pila."""
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
        capture[table_name, record_id] = __extract_column_values(
            db_metadata, record, columns
        )

        related_records = db_metadata.get_related_records(record)
        for related_record in related_records:
            stack.append(related_record)

    return dict(capture)


def capture_records(db_metadata: IDBMetadata, records: List[Any]) -> Capture:
    """Captura los registros proporcionados."""
    capture: Capture = defaultdict(dict)
    for record in records:
        table_name = db_metadata.get_table_name_from_record(record)
        record_id = db_metadata.get_record_id(record)
        columns = db_metadata.get_table_columns_from_record(record)

        capture[table_name, record_id] = __extract_column_values(
            db_metadata, record, columns
        )

    return dict(capture)


def capture_all_records(db_metadata: IDBMetadata, page_size: int = 1) -> Capture:
    """Captura todos los registros de la base de datos."""
    tables = db_metadata.get_tables()
    capture: Capture = defaultdict(dict)

    for table in tables:
        offset = 0
        columns = db_metadata.get_table_columns_from_table(table)
        table_name = db_metadata.get_table_name_from_table(table)

        while records := db_metadata.get_records(table, offset, page_size):

            for record in records:
                record_id = db_metadata.get_record_id(record)

                capture[table_name, record_id] = __extract_column_values(
                    db_metadata, record, columns
                )

            offset += page_size

    return dict(capture)


def __extract_column_values(
    db_metadata: IDBMetadata, record: Any, columns: List[Any]
) -> Dict[str, Any]:
    columns_values: Dict[str, Any] = defaultdict(dict)
    for column in columns:
        column_name = db_metadata.get_column_name(column)
        column_value = db_metadata.get_column_value(column_name, record)
        column_is_foreign_key = db_metadata.column_is_foreign_key(column)
        key = f"{column_name} (FK)" if column_is_foreign_key else column_name
        columns_values[key] = column_value
    return dict(columns_values)
