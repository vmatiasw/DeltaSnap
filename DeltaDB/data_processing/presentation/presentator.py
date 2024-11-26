from DeltaDB.types import ChangesProcessed
from typing import Dict, List


def ignore_diff_fields(changes: ChangesProcessed, fields: Dict[str, List[str]]) -> None:
    """
    Marks specified fields in the difference dictionary as 'ignored'.

    Args:
        changes (ChangesProcessed): A dictionary where the key is a tuple (table_name, table_id), and the value is a list of changes.
                                     Each change is represented as a tuple (field_name, old_value, new_value).
        fields (Dict[str, List[str]]): A dictionary where the key is a table name and the value is a list of field names
                                       that should be marked as 'ignored'.

    Example:
        Input changes = {('game_sessions', 1): [('turn_duration', 0, 60), ('started', False, True)]}
        
        Input fields = {'game_sessions': ['turn_duration']}
 
        Output = {('game_sessions', 1): [('turn_duration', 'ignored'), ('started', False, True)]}
    """
    for table_id, table_changes in changes.items():
        table_name = table_id[0]
        if table_name in fields:
            for i, change in enumerate(table_changes):
                for field in fields[table_name]:
                    if change[0] == field:
                        table_changes[i] = (change[0], 'ignored')
                        break


def remove_tables(changes: ChangesProcessed, table_names: List[str]) -> None:
    """
    Removes the specified tables from the 'changes' dictionary in place.

    Args:
        changes (ChangesProcessed): A dictionary where the key is a tuple (table_name, table_id) and the value is a list of changes.
        table_names (List[str]): A list of table names to be removed from the 'changes' dictionary.

    Example:
        Input changes = {('game_sessions', 1): [('turn_duration', 0, 60), ('started', False, True)]}
        
        Input table_names = ['game_sessions']

        Output = {}
    """
    keys_to_remove = [table_id for table_id in changes if table_id[0] in table_names]
    for table_id in keys_to_remove:
        changes.pop(table_id)
