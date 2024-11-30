from typing import Tuple

from DeltaDB.types import Capture, CreatedTables, DeletedTables, FieldsChanges, TablesChanges
from DeltaDB.data_processing.data_classes import Changes, Created, Deleted

# TODO: Al marcar algo se usa # en el valor, ... ¿es necesario? ¿es una buena práctica?

def diff_captures(initial_capture: Capture, final_capture: Capture) -> Tuple[Changes, Created, Deleted]:
    """
    Compares two capture dictionaries and identifies the differences between them, 
    categorizing them into changes, deletions, and creations.
    """
    changes: TablesChanges = {}
    deleted: DeletedTables = set()
    created: CreatedTables = set()

    # Detect deleted tables and analyze changes
    for table_key, initial_table in initial_capture.items():
        final_table = final_capture.get(table_key)
        if final_table is None:
            # Table was deleted
            deleted.add(table_key)
            continue

        # Track changes within the table
        current_changes: FieldsChanges = {}

        for column, initial_value in initial_table.items():
            if column not in final_table:
                current_changes[column] = (initial_value, "#column don't exist")
                continue
            
            final_value = final_table.get(column)
            if initial_value != final_value:
                current_changes[column] = (initial_value, final_value)
                
        for column, final_value in final_table.items():
            if column not in initial_table:
                current_changes[column] = ("#column don't exist", final_value)

        if current_changes:
            changes[table_key] = current_changes

    # Detect newly created tables
    for table_key in final_capture.keys():
        if table_key not in initial_capture:
            created.add(table_key)

    return Changes(changes), Created(created), Deleted(deleted)
