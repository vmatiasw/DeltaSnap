from typing import Dict, List, Set, Any
from collections import Counter, defaultdict
from abc import ABC, abstractmethod

from DeltaDB.types import CreatedTables, DeletedTables, TablesChanges, info

# TODO: agregar funciones para:
# - Devolver el diccionario de cambios invertido
# - Funciones que devuelvan el esquema de los datos en vez de recibir el esquema y devolver un booleano
# - eliminar ignore_diff_fields?, es mejor mokear

class __Data(ABC):
    def __init__(self, data: Any):
        self.data = data

    def __str__(self) -> str:
        return f"{self.data}"

    @abstractmethod
    def remove_tables(self, table_names: List[str]) -> "__Data":
        pass

    @abstractmethod
    def get_frequency(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def matches_schema(self, schema) -> bool:
        pass


class __DataSet(__Data):
    def __init__(self, data: Set):
        super().__init__(data)

    def remove_tables(self, table_names: List[str]) -> "__DataSet":
        table_names_set = set(table_names)
        self.data = {key for key in self.data if key[0] not in table_names_set}
        return self

    def get_frequency(self) -> Dict[str, int]:
        return dict(Counter([key[0] for key in self.data]))

    def matches_schema(self, schema: Set[str]) -> bool:
        data_tables = {tup[0] for tup in self.data}
        return data_tables == schema


class Deleted(__DataSet):
    def __init__(self, deleted: DeletedTables):
        super().__init__(deleted)


class Created(__DataSet):
    def __init__(self, created: CreatedTables):
        super().__init__(created)


class Changes(__Data):
    def __init__(self, changes: TablesChanges):
        super().__init__(changes)

    def ignore_diff_fields(self, fields: Dict[str, Set[str]]) -> "Changes":
        for table_id, table_changes in self.data.items():
            table_name = table_id[0]
            if table_name in fields:
                for field, _ in table_changes.items():
                    if field in fields[table_name]:
                        table_changes[field] = (info('change ignored'), info('change ignored'))
        return self

    def remove_tables(self, table_names: List[str]) -> "Changes":
        table_names_set = set(table_names)
        self.data = {key: value for key, value in self.data.items()
                     if key[0] not in table_names_set}
        return self

    def get_frequency(self) -> Dict[str, Dict[str, int]]:
        result: Dict[str, Dict[str, int]] = defaultdict(
            lambda: defaultdict(int))
        for (table_name, _), table_changes in self.data.items():
            result[table_name][info('table frequency')] += 1
            for field, _ in table_changes.items():
                result[table_name][field] += 1
        for defdict in result:
            result[defdict] = dict(result[defdict])
        return dict(result)

    def matches_schema(self, schema: Dict[str, List[str]]) -> bool:
        if set(self.data.keys()) != set(schema.keys()):
            return False

        for key, dict in self.data.items():
            fields = dict.keys()
            if fields != schema[key]:
                return False

        return True
