from typing import Any, List, Tuple, Dict, TypeVar, Set, NewType

from tests.db.models.sql_alchemy import Base  # FIXME: Change this import

BaseModel = TypeVar("BaseModel", bound=Base)  # SQLAlchemy models

RecordId = Tuple[str, int]  # (table_name, id)

Info = NewType("Info", str)


def info(value: str) -> Info:
    return Info("#" + value)


# Capture
Field = str
# { (table_name, id): {field_name: value} }
Capture = Dict[RecordId, Dict[Field, Any]]

# Changes Deleted Created
ValueChange = Tuple[Any, Any]  # (previous value, new value)
RecordChanges = Dict[Field, ValueChange]
RecordsChanges = Dict[RecordId, RecordChanges]
DeletedRecords = Set[RecordId]
CreatedRecords = Set[RecordId]

ModelsList = List[BaseModel]
