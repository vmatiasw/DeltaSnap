from typing import Any, List, Tuple, Dict, TypeVar, Set, NewType

from tests.db.models.sql_alchemy import Base  # FIXME: Change this import

BaseModel = TypeVar("BaseModel", bound=Base)  # SQLAlchemy models

UniqueTableId = Tuple[str, int]  # (table_name, id)

Info = NewType("Info", str)


def info(value: str) -> Info:
    return Info("#" + value)


# Capture
Field = str
# { (table_name, id): {column_name: value} }
Capture = Dict[UniqueTableId, Dict[Field, Any]]

# Changes Deleted Created
ValueChange = Tuple[Any, Any]  # (previous value, new value)
FieldsChanges = Dict[Field, ValueChange]
RecordsChanges = Dict[UniqueTableId, FieldsChanges]
DeletedRecords = Set[UniqueTableId]
CreatedRecords = Set[UniqueTableId]

ModelsList = List[BaseModel]
