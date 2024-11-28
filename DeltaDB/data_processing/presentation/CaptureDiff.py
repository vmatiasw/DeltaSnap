from typing import Dict, List
from collections import defaultdict

from DeltaDB.types import CreatedTables, DeletedTables, RawChanges

# TODO:
# - Agregar invertir el diccionario de cambios


class __Data():
    """
    Abstract base class that provides common functionality to represent data.
    """

    def __init__(self, data):
        self.data = data

    def __str__(self) -> str:
        return f"{self.data}"
    
    def remove_tables(self, table_names: List[str]) -> "__Data":
        """
        Removes the specified tables from the data structure. This operation is done in-place.
        """
        table_names_set = set(table_names)
        if isinstance(self.data, dict):
            self.data = {key: value for key, value in self.data.items() if key[0] not in table_names_set}
        elif isinstance(self.data, set):
            self.data = {key for key in self.data if key[0] not in table_names_set}
        return self
    
    def reduce_to_frecuency(self) -> "__Data":
        pass # TODO: Esto se hace mas facil si en vez de listas se usan diccionarios para _Changes y conjuntos para _Deleted y _Created
        return self

class _Changes(__Data):
    """
    Clase que maneja los cambios entre tablas.
    """

    def __init__(self, changes: RawChanges):
        super().__init__(changes)

    def ignore_diff_fields(self, fields: Dict[str, List[str]]) -> "_Changes":
        """
        Marks specified fields in the difference dictionary as 'ignored'. This method checks
        the changes and updates the specified fields to 'ignored', indicating that they should
        not be considered when comparing differences.

        Args:
            fields (Dict[str, List[str]]): A dictionary where the key is the table name, and the value
                                        is a list of field names to be marked as 'ignored'. The fields
                                        in the list will have their values replaced by ('ignored', 'ignored')
                                        in the changes.

        Returns:
            RawChanges: The updated dictionary with the ignored fields marked as 'ignored'.
        """
        for table_id, table_changes in self.data.items():
            table_name = table_id[0]
            if table_name in fields:
                for i, change in enumerate(table_changes):
                    for field in fields[table_name]:
                        if change[0] == field:
                            table_changes[i] = (
                                change[0], 'ignored', 'ignored')
                            break
        return self

class _Deleted(__Data):
    """
    Clase que maneja las tablas eliminadas.
    """

    def __init__(self, deleted: DeletedTables):
        super().__init__(deleted)

class _Created(__Data):
    """
    Clase que maneja las tablas creadas.
    """

    def __init__(self, created: CreatedTables):
        super().__init__(created)

class CaptureDiff:
    """
    Compara dos capturas y devuelve las diferencias: cambios, eliminados y creados.
    """

    def __init__(self, changes: RawChanges, deleted: DeletedTables, created: CreatedTables):
        self.changes = _Changes(changes)
        self.deleted = _Deleted(deleted)
        self.created = _Created(created)
    
    def remove_tables(self, table_names: List[str]) -> "CaptureDiff":
        """
        Removes the specified tables from the 'changes', 'deleted', and 'created' attributes in place.

        This method filters out any entries in the 'changes' dictionary, 'deleted' list, and 'created' list
        where the table name matches one of the names in the provided list 'table_names'. The operation is done
        in-place, and the attributes are updated directly.

        Args:
            table_names (List[str]): A list of table names to be removed from the 'changes', 'deleted', and 'created' attributes.
        """
        self.changes.remove_tables(table_names)
        self.deleted.remove_tables(table_names)
        self.created.remove_tables(table_names)

        return self

    def __str__(self) -> str:
        return f"{self.changes}, {self.deleted}, {self.created}"
