from typing import Tuple

from src.domain.types import (
    Capture,
    CreatedRecords,
    DeletedRecords,
    FieldsChanges,
    RecordsChanges,
    info,
)
from src.domain.data_processing.data_classes import Changes, Created, Deleted


def diff_records_captures(
    initial_capture: Capture, final_capture: Capture
) -> Tuple[Changes, Created, Deleted]:
    """
    Compares two capture dictionaries and identifies the differences between them,
    categorizing them into changes, deletions, and creations.
    """
    changes: RecordsChanges = {}
    deleted: DeletedRecords = set(initial_capture.keys()) - set(final_capture.keys())
    created: CreatedRecords = set(final_capture.keys()) - set(initial_capture.keys())

    # Detect changes in existing records
    for record_key, initial_record in initial_capture.items():
        final_record = final_capture.get(record_key)
        if not final_record:
            continue  # This table is in the deleted set

        current_changes: FieldsChanges = {}
        initial_columns = set(initial_record.keys())
        final_columns = set(final_record.keys())

        # Columns that were removed from the final capture
        removed_columns = initial_columns - final_columns
        for column in removed_columns:
            current_changes[column] = (
                initial_record[column],
                info("column don't exist"),
            )

        # Columns that were added to the final capture
        added_columns = final_columns - initial_columns
        for column in added_columns:
            current_changes[column] = (info("column don't exist"), final_record[column])

        # Columns that have changed
        common_columns = initial_columns & final_columns
        for column in common_columns:
            initial_value = initial_record[column]
            final_value = final_record[column]
            if initial_value != final_value:
                current_changes[column] = (initial_value, final_value)

        if current_changes:
            changes[record_key] = current_changes

    return Changes(changes), Created(created), Deleted(deleted)
