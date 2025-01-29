from __future__ import annotations
from typing import Dict, Set, Tuple
from collections import Counter, defaultdict

from src.deltasnap.domain.types import CreatedRecords, DeletedRecords


class BaseDataSet(set):
    def __init__(self, data: Set[Tuple[str, int]]):
        """
        Base class for datasets.

        :param data: A set of tuples containing table names and record IDs.
        """
        super().__init__(data)

    def remove_tables(self, table_names: Set[str]) -> BaseDataSet:
        """
        Removes records of the specified tables from the dataset.

        :param table_names: List of table names to remove from the dataset.
        :return: The updated dataset.
        """
        for table_name, record_id in self:
            if table_name in table_names:
                self.remove((table_name, record_id))

        # other approach: return type(self)({item for item in self if item[0] not in table_names})
        return self

    def get_frequency(self) -> Dict[str, int]:
        """
        Returns the frequency of each table in the dataset.

        :return: A dictionary mapping table names to their frequencies.
        """
        return Counter(key[0] for key in self)

    def get_schema(self) -> Set[str]:
        """
        Returns the unique table names in the dataset.

        :return: A set of table names.
        """
        return {table_name for table_name, _ in self}

    def get_inverted_capture(self) -> Dict[str, Set[str]]:
        """
        Returns the inverted capture of the dataset.

        :return: A dictionary mapping table names to sets of record IDs.
        """
        inverted_capture = defaultdict(set)
        for table_name, record_id in self:
            inverted_capture[table_name].add(record_id)
        return dict(inverted_capture)


class Deleted(BaseDataSet):
    def __init__(self, deleted: DeletedRecords):
        """
        Represents records marked as deleted.

        :param deleted: A set of tuples representing deleted records.
        """
        super().__init__(deleted)


class Created(BaseDataSet):
    def __init__(self, created: CreatedRecords):
        """
        Represents records marked as created.

        :param created: A set of tuples representing created records.
        """
        super().__init__(created)
