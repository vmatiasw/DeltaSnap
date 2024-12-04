from collections import defaultdict
from typing import Any, List

from src.domain.types import Capture
from src.domain.interfaces.IDBMetadata import IDBMetadata

# TODO:
# Agregar funcion que capture los registros pasados y cada uo de sus registros foraneos recursivamente
# No habria problema si se hace de manera recursiva, ya que se esta utilizando un diccionario y
# las claves son unicas, por lo que solo habria que parar cuando se llegue a un registro que ya se 
# haya capturado

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
