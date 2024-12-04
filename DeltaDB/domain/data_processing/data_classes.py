from __future__ import annotations
from typing import Dict, List, Set, Any
from collections import Counter, defaultdict

from DeltaDB.domain.types import CreatedRecords, DeletedRecords, RecordsChanges, info


class __Data:
    def __init__(self, data: Any):
        self.data = data

    def __str__(self) -> str:
        return f"{self.data}"


class __DataSet(__Data):
    def __init__(self, data: Set):
        super().__init__(data)

    def remove_tables(self, record_names: List[str]) -> __DataSet:
        """
        Removes records of the specified tables from the dataset.

        :param table_names: List of table names to remove from the dataset.
        :return: The updated dataset.
        """
        record_names_set = set(record_names)
        self.data = {key for key in self.data if key[0] not in record_names_set}
        return self

    def get_frequency(self) -> Dict[str, int]:
        """
        Returns the frequency of each table in the dataset.

        :return: A dictionary mapping table names to their frequencies.
        """
        return dict(Counter([key[0] for key in self.data]))

    def get_schema(self) -> Set[str]:
        """
        Returns the table names in the dataset.

        :return: A set of table names.
        """
        return {tup[0] for tup in self.data}


class Deleted(__DataSet):
    def __init__(self, deleted: DeletedRecords):
        super().__init__(deleted)


class Created(__DataSet):
    def __init__(self, created: CreatedRecords):
        super().__init__(created)


class Changes(__Data):
    def __init__(self, changes: RecordsChanges):
        super().__init__(changes)

    def ignore_fields_changes(self, fields: Dict[str, Set[str]]) -> Changes:
        """
        Ignores the changes in the specified fields of the specified tables.

        Note: Mocks changes is preferred than use this functio to removing them.

        :param fields_to_ignore: Dictionary where keys are table names and values are sets of field names to ignore.
        :return: The updated Changes object.
        """
        for (table_name, record_id), record_changes in self.data.items():
            if table_name in fields:
                for field, change in record_changes.items():
                    if field in fields[table_name]:
                        record_changes[field] = (
                            info("change ignored"),
                            info("change ignored"),
                        )
        return self

    def remove_tables(self, record_names: List[str]) -> Changes:
        """
        Removes records of the specified tables from the changes.

        :param table_names: List of table names to remove from the changes.
        :return: The updated Changes object.
        """
        record_names_set = set(record_names)
        self.data = {
            key: value
            for key, value in self.data.items()
            if key[0] not in record_names_set
        }
        return self

    def get_frequency(self) -> Dict[str, Dict[str, int]]:
        """
        Returns the frequency of each table and field in the changes.

        :return: A dictionary mapping table names to field frequencies.
        """
        result: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        for (table_name, record_id), record_changes in self.data.items():
            result[table_name][info("table frequency")] += 1
            for field, change in record_changes.items():
                result[table_name][field] += 1

        return {table: dict(fields) for table, fields in result.items()}

    def get_schema(self) -> Dict[str, Set[str]]:
        """
        Returns the table and field names of the changes.

        :return: A dictionary mapping table names to sets of field names.
        """
        schema: Dict[str, Set[str]] = defaultdict(set)
        for (table_name, record_id), changes_dict in self.data.items():
            schema[table_name] |= set(changes_dict.keys())
        return dict(schema)
