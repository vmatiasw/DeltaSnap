from DeltaDB.types import Capture, CreatedTables, DeletedTables, FieldsChanges, TablesChanges
from DeltaDB.data_processing.CaptureDiff import CaptureDiff


def diff_captures(initial_capture: Capture, final_capture: Capture) -> CaptureDiff:
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

        # Ensure consistency in structure FIXME: Eliminar asserts (cuando podria suceder este escenario?)
        assert len(initial_table) == len(final_table), "Column count mismatch between captures."

        # Track changes within the table
        current_changes: FieldsChanges = {}

        for column, initial_value in initial_table.items():
            final_value = final_table.get(column)
            if final_value is None:
                raise ValueError(
                    f"Column '{column}' in table {table_key} not found in the final metadata.")

            if initial_value != final_value:
                current_changes[column] = (initial_value, final_value)

        if current_changes:
            changes[table_key] = current_changes

    # Detect newly created tables
    for table_key in final_capture.keys():
        if table_key not in initial_capture:
            created.add(table_key)

    return CaptureDiff(changes, deleted, created)
