from typing import Dict, Tuple, List
from DeltaDB.types import Capture, Changes, Deleted, Created

def compare_captures(initial_metadata: Capture, final_metadata: Capture) -> Tuple[Changes, Deleted, Created]:
    """
    Compares two capture dictionaries and returns:
        - A dictionary with changes detected between tables in both captures.
        - A list of deleted tables present in the initial metadata but not in the final.
        - A list of newly created tables present in the final metadata but not in the initial.

    Args:
        initial_metadata (Capture): The metadata dictionary from the initial capture.
        final_metadata (Capture): The metadata dictionary from the final capture.

    Returns:
        Tuple[Changes, Deleted, Created]: 
            - Changes: A dictionary with table keys and a list of changes per table.
            - Deleted: A sorted list of deleted tables.
            - Created: A sorted list of newly created tables.

    Example:
        initial_metadata = {
            ('table1', id1): {'key1': value1, 'key2': value2},
            ('table2', id2): {'key1': value1, 'key2': value2}
        }
        
        final_metadata = {
            ('table1', id1): {'key1': modified_value1, 'key2': value2},
            ('table3', id3): {'key1': value1, 'key2': value2}
        }
        
        Returns:
        - Changes: {('table1', id1): [('key1', value1, modified_value1)]}
        - Deleted: [('table2', id2)]
        - Created: [('table3', id3)]
    """
    changes: Changes = {}
    deleted: Deleted = []
    created: Created = []

    # Detect deleted tables and analyze changes
    for table_key, initial_table in initial_metadata.items():
        final_table = final_metadata.get(table_key)
        
        if final_table is None:
            # Table was deleted
            deleted.append(table_key)
            continue
        
        # Ensure consistency in structure
        assert len(initial_table) == len(final_table), "Column count mismatch between captures."
        assert isinstance(table_key, tuple) and len(table_key) == 2, \
            f"Table key must be a tuple (table_name, id). Found: {type(table_key)}"
        assert isinstance(table_key[0], str), "First element of table key must be a string (table_name)."
        assert isinstance(table_key[1], int), "Second element of table key must be an integer (id)."

        # Track changes within the table
        current_changes = []

        for column, initial_value in initial_table.items():
            final_value = final_table.get(column)
            if final_value is None:
                raise ValueError(f"Column '{column}' in table {table_key} not found in the final metadata.")
            
            if initial_value != final_value:
                current_changes.append((column, initial_value, final_value))

        if current_changes:
            changes[table_key] = current_changes

    # Detect newly created tables
    for table_key in final_metadata.keys():
        if table_key not in initial_metadata:
            created.append(table_key)

    # Sort the results
    deleted.sort()
    created.sort()
    for change_list in changes.values():
        change_list.sort()

    return changes, deleted, created
