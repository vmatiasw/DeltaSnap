from typing import List, Any, Tuple

from DeltaDB.infrastructure.configurations.DBConfig import DBConfig
from DeltaDB.domain.data_processing.ingestion import (
    capture_all_records,
    capture_records,
    capture_related_records,
)
from DeltaDB.domain.data_processing.analysis import compare_capture
from DeltaDB.domain.types import Capture
from DeltaDB.domain.data_processing.data_classes.Changes import Changes
from DeltaDB.domain.data_processing.data_classes.data_sets import Created, Deleted


class DBCapturer:
    """
    A class for capturing the structure and data of database.

    Args:
        configurator: An instance of DatabaseConfigurator with the necessary settings.
    """

    def __init__(self, configurator: DBConfig):
        self.db_metadata = configurator.get_db_metadata_adapter()

    def capture_all_records(self, page_size: int = 1000) -> Capture:
        """
        Captures the structure and data of all tables in the database.

        Args:
            page_size (int): The number of records to capture per page.

        Returns:
            object: The capture result.
        """
        return capture_all_records(self.db_metadata, page_size)

    def capture_records(self, records: List[Any]) -> Capture:
        """
        Captures the structure and data of the specified records.

        Args:
            records (object): The records to be captured.

        Returns:
            object: The capture result.
        """
        return capture_records(self.db_metadata, records)

    def capture_related_records(self, records: List[Any]) -> Capture:
        """
        Captures the structure and data of the specified records and their related records.

        Args:
            records (object): The records to be captured.

        Returns:
            object: The capture result.
        """
        return capture_related_records(self.db_metadata, records)

    @staticmethod
    def compare_capture(
        initial_capture: Capture, final_capture: Capture
    ) -> Tuple[Changes, Created, Deleted]:
        """
        Compares two data captures and identifies the differences between them,
        categorizing them into changes, deletions, and creations.

        Args:
            initial_capture (object): The initial data capture.
            final_capture (object): The final data capture.

        Returns:
            object: The result of the capture comparison.
        """
        return compare_capture(initial_capture, final_capture)
