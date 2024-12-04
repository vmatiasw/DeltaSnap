from collections import defaultdict
from typing import Any, List

from src.domain.types import Capture
from src.domain.interfaces.IDBMetadata import IDBMetadata


def capture_related_records(db_metadata: IDBMetadata, records: List[Any]) -> Capture:
    metadata: Capture = defaultdict(dict)
    for record in records:
        __capture_related_records(db_metadata, record, metadata)
    return dict(metadata)


def __capture_related_records(
    db_metadata: IDBMetadata, record: Any, metadata: Capture
) -> None:
    table_name = db_metadata.get_table_name_from_record(record)
    record_id = db_metadata.get_record_id(record)
    if metadata.get((table_name, record_id)):
        return

    columns = db_metadata.get_table_columns_from_record(record)

    __capture_record_columns(
        db_metadata, record, metadata, table_name, record_id, columns
    )

    related_records = db_metadata.get_related_records(record)
    for related_record in related_records:
        __capture_related_records(db_metadata, related_record, metadata)


def capture_records(db_metadata: IDBMetadata, records: List[Any]) -> Capture:
    metadata: Capture = defaultdict(dict)
    for record in records:
        table_name = db_metadata.get_table_name_from_record(record)
        record_id = db_metadata.get_record_id(record)
        columns = db_metadata.get_table_columns_from_record(record)

        __capture_record_columns(
            db_metadata, record, metadata, table_name, record_id, columns
        )

    return dict(metadata)


def capture_all_records(db_metadata: IDBMetadata, page_size: int = 1) -> Capture:
    tables = db_metadata.get_tables()
    metadata: Capture = defaultdict(dict)

    for table in tables:
        offset = 0
        columns = db_metadata.get_table_columns_from_table(table)
        table_name = db_metadata.get_table_name_from_table(table)

        while records := db_metadata.get_records(table, offset, page_size):

            for record in records:
                record_id = db_metadata.get_record_id(record)

                __capture_record_columns(
                    db_metadata, record, metadata, table_name, record_id, columns
                )

            offset += page_size

    return dict(metadata)


def __capture_record_columns(
    db_metadata, record, metadata, table_name, record_id, columns
):
    for column in columns:
        column_name = db_metadata.get_column_name(column)
        column_value = db_metadata.get_column_value(column_name, record)
        column_is_foreign_key = db_metadata.column_is_foreign_key(column)
        key = f"{column_name} (FK)" if column_is_foreign_key else column_name
        metadata[table_name, record_id][key] = column_value
