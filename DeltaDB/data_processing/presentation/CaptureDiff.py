from typing import Dict, List, Set, Any
from collections import Counter, defaultdict
from abc import ABC, abstractmethod

from DeltaDB.types import CreatedTables, DeletedTables, TablesChanges

# TODO:
# - Agregar invertir el diccionario de cambios


class __Data(ABC):
    def __init__(self, data: Any):
        self.data = data

    def __str__(self) -> str:
        return f"{self.data}"

    @abstractmethod
    def remove_tables(self, table_names: List[str]) -> "__Data":
        pass

    @abstractmethod
    def get_frecuency(self) -> Dict[str, Any]:
        pass


class __DataSet(__Data):
    def __init__(self, data: Set):
        super().__init__(data)

    def remove_tables(self, table_names: List[str]) -> "__Data":
        table_names_set = set(table_names)
        self.data = {key for key in self.data if key[0] not in table_names_set}
        return self

    def get_frecuency(self) -> Dict[str, int]:
        return dict(Counter([key[0] for key in self.data]))


class _Deleted(__DataSet):
    def __init__(self, deleted: DeletedTables):
        super().__init__(deleted)


class _Created(__DataSet):
    def __init__(self, created: CreatedTables):
        super().__init__(created)


class _Changes(__Data):
    def __init__(self, changes: TablesChanges):
        super().__init__(changes)

    def ignore_diff_fields(self, fields: Dict[str, Set[str]]) -> "_Changes":
        for table_id, table_changes in self.data.items():
            table_name = table_id[0]
            if table_name in fields:
                for field, _ in table_changes.items():
                    if field in fields[table_name]:
                        table_changes[field] = ('#ignored', '#ignored')
        return self

    def remove_tables(self, table_names: List[str]) -> "__Data":
        table_names_set = set(table_names)
        self.data = {key: value for key, value in self.data.items()
                     if key[0] not in table_names_set}
        return self

    def get_frecuency(self) -> Dict[str, Dict[str, int]]:
        result : Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for (table_name, _), table_changes in self.data.items():
            result[table_name]['#table frecuency'] += 1
            for field, _ in table_changes.items():
                result[table_name][field] += 1
        for defdict in result:
            result[defdict] = dict(result[defdict])
        return dict(result)


class CaptureDiff:
    def __init__(self, changes: TablesChanges, deleted: DeletedTables, created: CreatedTables):
        self.changes = _Changes(changes)
        self.deleted = _Deleted(deleted)
        self.created = _Created(created)

    def remove_tables(self, table_names: List[str]) -> "CaptureDiff":
        self.changes.remove_tables(table_names)
        self.deleted.remove_tables(table_names)
        self.created.remove_tables(table_names)
        return self

    def __str__(self) -> str:
        return f"{self.changes}, {self.deleted}, {self.created}"
