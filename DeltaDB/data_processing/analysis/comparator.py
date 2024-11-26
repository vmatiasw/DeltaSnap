from typing import Tuple, List
from DeltaDB.types import Capture, Changes, Deleted, Created, Change

def diff_captures(initial_capture: Capture, final_capture: Capture) -> Tuple[Changes, Deleted, Created]:
    """
    Compares two capture dictionaries and identifies differences between them, including:
        - Changes within tables present in both captures.
        - Tables deleted from the initial capture.
        - Tables newly created in the final capture.

    Args:
        initial_capture (Capture): A dictionary representing the initial state of captures.
        final_capture (Capture): A dictionary representing the final state of captures.

    Returns:
        Tuple(Tuple[Changes, Deleted, Created]):
            - Changes: A dictionary where each key is a table identifier and each value is a list of 
                       column-level changes in the format (column, old_value, new_value).
            - Deleted: A sorted list of table identifiers present in the initial capture but absent in the final.
            - Created: A sorted list of table identifiers present in the final capture but absent in the initial.

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
            Changes: {('table1', id1): [('key1', value1, modified_value1)]}
            Deleted: [('table2', id2)]
            Created: [('table3', id3)]
    """
    changes: Changes = {}
    deleted: Deleted = []
    created: Created = []

    # Detect deleted tables and analyze changes
    for table_key, initial_table in initial_capture.items():
        final_table = final_capture.get(table_key)
        
        if final_table is None:
            # Table was deleted
            deleted.append(table_key)
            continue
        
        # Ensure consistency in structure
        assert len(initial_table) == len(final_table), "Column count mismatch between captures."

        # Track changes within the table
        current_changes : List[Change] = []

        for column, initial_value in initial_table.items():
            final_value = final_table.get(column)
            if final_value is None:
                raise ValueError(f"Column '{column}' in table {table_key} not found in the final metadata.")
            
            if initial_value != final_value:
                current_changes.append((column, initial_value, final_value))

        if current_changes:
            changes[table_key] = current_changes

    # Detect newly created tables
    for table_key in final_capture.keys():
        if table_key not in initial_capture:
            created.append(table_key)

    # Sort the results
    deleted.sort()
    created.sort()
    for change_list in changes.values():
        change_list.sort()

    return changes, deleted, created
