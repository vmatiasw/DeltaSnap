from collections import defaultdict

from src.domain.types import Capture
from src.domain.interfaces.IDBMetadata import IDBMetadata

# TODO:
# Eliminar acoplamiento de la sesión de la base de datos
# Agregar funcion que solo capture los registros que le pasen
# Agregar funcion que capture un registro y sus relaciones (mas de uno tm? o habra probelmas con duplicados?)

def capture_all_tables(db_metadata:IDBMetadata, page_size: int = 1) -> Capture:
    tables = db_metadata.get_tables()
    metadata: Capture = defaultdict(dict)

    for table in tables:
        offset = 0
        columns = db_metadata.get_columns(table)
        table_name = db_metadata.get_table_name(table)
        
        while instances := db_metadata.get_instances(table, offset, page_size):
            
            for record in instances:
                record_id = db_metadata.get_record_id(record)
                
                for column in columns:
                    column_name = db_metadata.get_column_key(column)
                    column_value = db_metadata.get_column_value(column_name, record)
                    column_is_foreign_key = db_metadata.column_is_foreign_key(column)

                    key = f'{column_name} (FK)' if column_is_foreign_key else column_name
                    metadata[table_name, record_id][key] = column_value

            offset += page_size

    return dict(metadata)

#  # TODO: Actualizar esta funcion
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
