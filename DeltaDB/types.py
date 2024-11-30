from typing import Any, List, Tuple, Dict, TypeVar, Set, NewType

from tests.db.models.sql_alchemy import Base # FIXME: Change this import

BaseModel = TypeVar('BaseModel', bound=Base)  # SQLAlchemy models

UniqueTableId = Tuple[str, int]  # (table_name, id)

Message = NewType('Message', str)
def message(value: str) -> Message:
    return Message('#'+value)

# Capture
Field = str
Capture = Dict[UniqueTableId, Dict[Field, Any]] # { (table_name, id): {column_name: value} }

# Changes Deleted Created
ValueChange = Tuple[Any, Any] # (previous value, new value)
FieldsChanges = Dict[Field, ValueChange]
TablesChanges = Dict[UniqueTableId, FieldsChanges]
DeletedTables = Set[UniqueTableId]
CreatedTables = Set[UniqueTableId]

# Generic object and model lists
T = TypeVar('T') # Generic types
ObjectsList = List[T]
ModelsList = List[BaseModel]
