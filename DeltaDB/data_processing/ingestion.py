from collections import defaultdict

from tests.tools.db.database_connector import db_metedata_adapter
from DeltaDB.types import Capture#, ObjectsList
# from DeltaDB.validations import validate_data, ValidateId, ValidateInstance, ValidateTablename
#
# # List of validation rules to apply to objects
# capture_validations = [ValidateId(), ValidateInstance(), ValidateTablename()]
#
# def capture(objects: ObjectsList) -> Capture:
#     validate_data(objects, capture_validations)

#     metadata: Capture = defaultdict(dict)
    
#     for obj in objects:
#         inspected_obj = inspect(obj)

#         for column in inspected_obj.mapper.columns:
#             column_name = column.key
#             column_value = getattr(obj, column_name)

#             key = f'{column_name} (FK)' if column.foreign_keys else column_name
#             metadata[obj.__tablename__, obj.id][key] = column_value

#     return dict(metadata)

def capture_all_tables(session, page_size: int = 1) -> Capture:
    tables = db_metedata_adapter.get_tables()
    metadata: Capture = defaultdict(dict)

    for table in tables:
        offset = 0
        columns = db_metedata_adapter.get_columns(table)
        table_name = db_metedata_adapter.get_table_name(table)
        while instances := db_metedata_adapter.get_instances(session, table, offset, page_size):
            for record in instances:
                record_id = db_metedata_adapter.get_record_id(record)
                for column in columns:
                    column_name = db_metedata_adapter.get_column_key(column)
                    column_value = db_metedata_adapter.get_column_value(column_name, record)
                    column_is_foreign_key = db_metedata_adapter.column_is_foreign_key(column)

                    key = f'{column_name} (FK)' if column_is_foreign_key else column_name
                    metadata[table_name, record_id][key] = column_value
            
            offset += page_size
            
    return dict(metadata)