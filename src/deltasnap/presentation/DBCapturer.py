from typing import List, Any, Tuple

from src.deltasnap.infrastructure.configurations.DBConfig import DBConfig
from src.deltasnap.domain.data_processing.ingestion import (
    capture_all_records,
    capture_records,
    capture_related_records,
)
from src.deltasnap.domain.data_processing.analysis import compare_capture
from src.deltasnap.domain.types import Capture
from src.deltasnap.domain.data_classes.Changes import Changes
from src.deltasnap.domain.data_classes.data_sets import Created, Deleted


class DBCapturer:
    """
    A class for capturing the structure and data of the database.

    Args:
        configurator: An instance of DBConfig with the necessary settings.
    """

    def __init__(self, configurator: DBConfig):
        self.db_metadata = configurator._get_db_metadata_adapter()

    def capture_all_records(self, page_size: int = 1000) -> Capture:
        """
        Captures the structure and data of all tables in the database.

        Args:
            page_size (int): The number of records to capture per page.

        Returns:
            Capture: The capture result.
        """
        return capture_all_records(self.db_metadata, page_size)

    def capture_records(self, records: List[Any]) -> Capture:
        """
        Captures the structure and data of the specified records.

        Args:
            records (List[Any]): The records to be captured.

        Returns:
            Capture: The capture result.
        """
        return capture_records(self.db_metadata, records)

    def capture_related_records(self, records: List[Any]) -> Capture:
        """
        Captures the structure and data of the specified records and their related records.

        Args:
            records (List[Any]): The records to be captured.

        Returns:
            Capture: The capture result.
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
            initial_capture (Capture): The initial data capture.
            final_capture (Capture): The final data capture.

        Returns:
            Tuple[Changes, Created, Deleted]: The result of the capture comparison.
        """
        return compare_capture(initial_capture, final_capture)
