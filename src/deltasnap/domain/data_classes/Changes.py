from __future__ import annotations
from typing import Dict, Set
from collections import defaultdict

from src.deltasnap.domain.types import RecordsChanges, info


class Changes(dict):
    def __init__(self, changes: RecordsChanges):
        super().__init__(changes)

    def ignore_fields_changes(self, fields_to_ignore: Dict[str, Set[str]]) -> Changes:
        """
        Ignores the changes in the specified fields of the specified tables.

        Note: Mocks changes is preferred than use this functio to removing them.

        :param fields_to_ignore: Dictionary where keys are table names and values are sets of field names to ignore.
        :return: The updated Changes object.
        """
        for (table_name, _), record_changes in self.items():
            if table_name in fields_to_ignore.keys():
                for field, _ in record_changes.items():
                    if field in fields_to_ignore[table_name]:
                        record_changes[field] = (
                            info("change ignored"),
                            info("change ignored"),
                        )
        return self

    def remove_tables(self, table_names: Set[str]) -> Changes:
        """
        Removes records of the specified tables from the changes.

        :param table_names: List of table names to remove from the changes.
        :return: The updated Changes object.
        """
        old_dict = self.copy()
        for (table_name, record_id), _ in old_dict.items():
            if table_name in table_names:
                self.pop((table_name, record_id))

        return self

    def get_frequency(self) -> Dict[str, Dict[str, int]]:
        """
        Returns the frequency of each table and field in the changes.

        :return: A dictionary mapping table names to field frequencies.
        """
        result: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        for (table_name, _), record_changes in self.items():
            result[table_name][info("table frequency")] += 1
            for field, _ in record_changes.items():
                result[table_name][field] += 1

        return {table: dict(fields) for table, fields in result.items()}

    def get_schema(self) -> Dict[str, Set[str]]:
        """
        Returns the table and field names of the changes.

        :return: A dictionary mapping table names to sets of field names.
        """
        schema: Dict[str, Set[str]] = defaultdict(set)

        for (table_name, _), changes_dict in self.items():
            schema[table_name].update(changes_dict.keys())

        return dict(schema)

    def get_inverted_capture(self) -> Dict[str, Dict[str, Set[str]]]:
        """
        Returns the inverted capture of the changes.

        :return: A dictionary mapping table names to dictionaries of field names and record ids.
        """
        inverted_capture: Dict[str, Dict[str, Set[str]]] = defaultdict(
            lambda: defaultdict(set)
        )

        for (table_name, record_id), record_changes in self.items():
            for field, _ in record_changes.items():
                inverted_capture[table_name][field].add(record_id)

        return {table: dict(fields) for table, fields in inverted_capture.items()}
