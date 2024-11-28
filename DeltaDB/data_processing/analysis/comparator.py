from DeltaDB.types import Capture, CreatedTables, DeletedTables, FieldsChanges, TablesChanges, ValueChange
from DeltaDB.data_processing.presentation.CaptureDiff import CaptureDiff


def diff_captures(initial_capture: Capture, final_capture: Capture) -> CaptureDiff:
    """
    Compares two capture dictionaries and identifies the differences between them, 
    categorizing them into changes, deletions, and creations.

    The function performs the following:
        - Identifies changes in tables present in both captures (column-level changes).
        - Identifies tables deleted in the initial capture but not present in the final capture.
        - Identifies tables newly created in the final capture that are absent in the initial capture.

    Args:
        initial_capture (Capture): A dictionary representing the initial state of captures, 
                                    where the keys are table identifiers and the values are dictionaries of column data.
        final_capture (Capture): A dictionary representing the final state of captures, 
                                  with the same structure as `initial_capture`.

    Returns:
        CaptureDiff: An object encapsulating the differences:
        - changes: A dictionary where each key is a unique table identifier (tuple of table name and ID),
                    and each value is a list of changes (tuples of column name, old value, and new value).
        - deleted: A list of table identifiers (tuples of table name and ID) that were present in the 
                    initial capture but are absent in the final.
        - created: A list of table identifiers (tuples of table name and ID) that are present in the final 
                    capture but were absent in the initial.

    Example:
        initial_capture = {
            ('table1', id1): {'key1': value1, 'key2': value2},
            ('table2', id2): {'key1': value1, 'key2': value2}
        }
        
        final_capture = {
            ('table1', id1): {'key1': modified_value1, 'key2': value2},
            ('table3', id3): {'key1': value1, 'key2': value2}
        }
        
        Output:
            changes: {('table1', id1): [('key1', value1, modified_value1)]}
            deleted: [('table2', id2)]
            created: [('table3', id3)]

    Notes:
        - This function assumes that the column structure is consistent across the tables in both captures.
        - If the column structure between captures differs, an AssertionError will be raised.
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

        # Ensure consistency in structure
        assert len(initial_table) == len(
            final_table), "Column count mismatch between captures."

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
