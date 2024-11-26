from typing import Any, List, Tuple, Dict, TypeVar, Literal, Union
from DB.SqlAlchemyDB.models import Base

# Generic types
T = TypeVar('T')
BaseModel = TypeVar('BaseModel', bound=Base)  # SQLAlchemy models

UniqueTable = Tuple[str, int]  # (table_name, id)

# Capture
Capture = Dict[UniqueTable, Dict[str, Tuple[Any,bool]]] # { (table_name, id): {column_name: (value, is_FK)} }

# Changes Deleted Created
RawChange = Tuple[str, Any, Any] # (column, previous value, new value)
RawChanges = Dict[UniqueTable, List[RawChange]]
DeletedTables = List[UniqueTable]
CreatedTables = List[UniqueTable]

# Generic object and model lists
ObjectsList = List[T]
ModelsList = List[BaseModel]
