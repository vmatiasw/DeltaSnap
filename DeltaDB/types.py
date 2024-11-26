from typing import Any, List, Tuple, Dict, TypeVar, Literal, Union
from DB.SqlAlchemyDB.models import Base

# Generic types
T = TypeVar('T')
BaseModel = TypeVar('BaseModel', bound=Base)  # SQLAlchemy models

UniqueTable = Tuple[str, int]  # (table_name, id)

# Capture
Capture = Dict[UniqueTable, Dict[str, Tuple[Any,bool]]] # { (table_name, id): {column_name: (value, is_FK)} }

# Changes
ChangePatch = Tuple[str, Literal['ignored']]
Change = Tuple[str, Any, Any] # (column, previous value, new value)
ChangesProcessed = Dict[UniqueTable, List[Union[Change, ChangePatch]]]
Changes = Dict[UniqueTable, List[Change]]
Deleted = List[UniqueTable]
Created = List[UniqueTable]

# Generic object and model lists
ObjectsList = List[T]
ModelsList = List[BaseModel]
