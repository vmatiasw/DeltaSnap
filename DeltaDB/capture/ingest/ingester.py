from sqlalchemy import inspect
from sqlalchemy.orm import Session

from DB.SqlAlchemyDB.db_setup import Base
from DeltaDB.types import Capture, ObjectsList, ModelsList
from DeltaDB.validations import validate_data, ValidateId, ValidateInstance, ValidateTablename

# List of validation rules to apply to objects
capture_validations = [ValidateId(), ValidateInstance(), ValidateTablename()]

def get_all_tables(session: Session, models: ModelsList = []) -> list:
    '''
    Returns instances of database tables.

    Args:
        session (Session): Active database session.
        models (ModelsList): Optional list of specific models to query.

    Returns:
        list: Instances of the queried models.
    '''
    all_instances = []
    mappers = Base.registry.mappers if models == [] else (model.__mapper__ for model in models)

    for mapper in mappers:
        instances = session.query(mapper.class_).all()
        all_instances.extend(instances)

    return all_instances

def capture(objects: ObjectsList) -> Capture:
    '''
    Returns a dictionary where each key is a tuple (__tablename__, id)
    and the value is a dictionary containing the table's metadata. 
    The keys are column names, and the values are their respective values in the object.

    Note: You might need to clear the cache to get updated metadata.

    Args:
        objects (ObjectsList): List of objects to capture metadata from.

    Returns:
        Capture: A dictionary with metadata for the captured objects.
    '''
    validate_data(objects, capture_validations)
    metadata: Capture = {}
    
    for obj in objects:
        metadata[obj.__tablename__, obj.id] = {}

        for column in inspect(obj).mapper.columns:
            column_name = column.key
            column_value = getattr(obj, column_name)

            if column.foreign_keys:
                metadata[obj.__tablename__, obj.id][f'{column_name} (FK)'] = column_value
            else:
                metadata[obj.__tablename__, obj.id][column_name] = column_value

    return metadata
