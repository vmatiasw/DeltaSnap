from DeltaDB.types import Changes
from typing import Dict, List


def ignore_field_values(changes: Changes, fields: Dict[str, List[str]]) -> None:
    '''
    Marks the changes in specified loose fields as 'ignored' for the tables listed in 'changes'.

    Args:
        changes (dict): A dictionary containing changes in various tables, where each key is a tuple (table_name, table_id)
                         and the value is a list of changes (field_name, old_value, new_value).
        fields (dict): A dictionary where keys are table names and values are lists of fields that should be ignored.

    Example:
        changes = {('game_sessions', 1): [('turn_duration', 0, 60), ('started', False, True)]}
        fields = {'game_sessions': ['turn_duration']}
        ignore_field_values(changes, fields)
        print(changes)  # Output: {('game_sessions', 1): [('turn_duration', 'ignored'), ('started', False, True)]}
    '''
    for table_id, table_changes in changes.items():
        table_name = table_id[0]
        if table_name in fields:
            for i, change in enumerate(table_changes):
                for field in fields[table_name]:
                    if change[0] == field:
                        table_changes[i] = (change[0], 'ignored')
                        break


def remove_tables(changes: Changes, tables: List[str]) -> None:
    '''
    Removes the specified tables from the 'changes' dictionary.

    Args:
        changes (dict): A dictionary containing changes for various tables.
        tables (list): A list of table names to be removed from 'changes'.

    Example:
        changes = {('game_sessions', 1): [('turn_duration', 0, 60), ('started', False, True)]}
        tables = ['game_sessions']
        remove_tables(changes, tables)
        print(changes)  # Output: {}
    '''
    keys_to_remove = [
        table_id for table_id in changes if table_id[0] in tables]
    for table_id in keys_to_remove:
        changes.pop(table_id)
