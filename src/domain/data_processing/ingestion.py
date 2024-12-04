from collections import defaultdict
from typing import Any, List

from src.domain.types import Capture
from src.domain.interfaces.IDBMetadata import IDBMetadata

# TODO:
# Agregar funcion que solo capture los registros que le pasen
# Agregar funcion que capture un registro y sus relaciones (mas de uno tm? o habra probelmas con duplicados?)


def capture_records(db_metadata: IDBMetadata, records: List[Any]) -> Capture:
    metadata: Capture = defaultdict(dict)
    for record in records:
        table_name = db_metadata.get_table_name_from_record(record)
        record_id = db_metadata.get_record_id(record)
        columns = db_metadata.get_table_columns_from_record(record)

        for column in columns:
            column_name = db_metadata.get_column_name(column)
            column_value = db_metadata.get_column_value(column_name, record)
            column_is_foreign_key = db_metadata.column_is_foreign_key(column)
            key = f"{column_name} (FK)" if column_is_foreign_key else column_name
            metadata[table_name, record_id][key] = column_value

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

                for column in columns:
                    column_name = db_metadata.get_column_name(column)
                    column_value = db_metadata.get_column_value(column_name, record)
                    column_is_foreign_key = db_metadata.column_is_foreign_key(column)

                    key = (
                        f"{column_name} (FK)" if column_is_foreign_key else column_name
                    )
                    metadata[table_name, record_id][key] = column_value

            offset += page_size

    return dict(metadata)
