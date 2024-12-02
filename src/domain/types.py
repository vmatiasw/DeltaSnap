from typing import Any, List, Tuple, Dict, TypeVar, Set, NewType

from tests.db.models.sql_alchemy import Base # FIXME: Change this import

BaseModel = TypeVar('BaseModel', bound=Base)  # SQLAlchemy models

UniqueTableId = Tuple[str, int]  # (table_name, id)

Info = NewType('Info', str)
def info(value: str) -> Info:
    return Info('#'+value)

# Capture
Field = str
Capture = Dict[UniqueTableId, Dict[Field, Any]] # { (table_name, id): {column_name: value} }

# Changes Deleted Created
ValueChange = Tuple[Any, Any] # (previous value, new value)
FieldsChanges = Dict[Field, ValueChange]
TablesChanges = Dict[UniqueTableId, FieldsChanges]
DeletedTables = Set[UniqueTableId]
CreatedTables = Set[UniqueTableId]

ModelsList = List[BaseModel]
