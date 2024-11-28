from typing import Any, List, Tuple, Dict, TypeVar, Set

from tests.tools.db.models.sql_alchemy import Base # FIXME: Change this import

BaseModel = TypeVar('BaseModel', bound=Base)  # SQLAlchemy models

UniqueTableId = Tuple[str, int]  # (table_name, id)

# Capture
Field = str
Capture = Dict[UniqueTableId, Dict[Field, Tuple[Any,bool]]] # { (table_name, id): {column_name: (value, is_FK)} }

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
