from typing import Any, Tuple, Dict, Set, NewType

Info = NewType("Info", str)


def info(value: str) -> Info:
    return Info("#" + value)


RecordId = Tuple[str, int]  # (table_name, id)
Field = str
Capture = Dict[RecordId, Dict[Field, Any]]  # { (table_name, id): {field_name: value} }

# Changes Deleted Created
ValueChange = Tuple[Any, Any]  # (previous value, new value)
RecordChanges = Dict[Field, ValueChange]
RecordsChanges = Dict[RecordId, RecordChanges]
DeletedRecords = Set[RecordId]
CreatedRecords = Set[RecordId]
