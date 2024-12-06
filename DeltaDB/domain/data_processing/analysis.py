from typing import Tuple

from DeltaDB.domain.types import (
    Capture,
    CreatedRecords,
    DeletedRecords,
    RecordChanges,
    RecordsChanges,
    info,
)
from DeltaDB.domain.data_processing.data_classes.Changes import Changes
from DeltaDB.domain.data_processing.data_classes.data_sets import Created, Deleted


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
    deleted: DeletedRecords = set(initial_capture.keys()) - set(final_capture.keys())
    created: CreatedRecords = set(final_capture.keys()) - set(initial_capture.keys())
    changes: RecordsChanges = __extract_records_changes(initial_capture, final_capture)

    return Changes(changes), Created(created), Deleted(deleted)


def __extract_records_changes(initial_capture: Capture, final_capture: Capture):
    """
    Extracts the changes between two captures.
    """
    changes: RecordsChanges = {}

    for record_key, initial_record in initial_capture.items():
        final_record = final_capture.get(record_key)
        if not final_record:
            continue  # This table is deleted

        record_changes: RecordChanges = {}
        initial_fields = set(initial_record.keys())
        final_fields = set(final_record.keys())

        # fields that were removed from the final capture
        removed_fields = initial_fields - final_fields
        for field in removed_fields:
            record_changes[field] = (initial_record[field], info("field don't exist"))

        # fields that were added to the final capture
        added_fields = final_fields - initial_fields
        for field in added_fields:
            record_changes[field] = (info("field don't exist"), final_record[field])

        # fields that have changed
        common_fields = initial_fields & final_fields
        for field in common_fields:
            initial_value = initial_record[field]
            final_value = final_record[field]
            if initial_value != final_value:
                record_changes[field] = (initial_value, final_value)

        if record_changes:
            changes[record_key] = record_changes

    return changes
