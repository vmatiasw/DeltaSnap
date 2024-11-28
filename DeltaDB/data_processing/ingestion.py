from sqlalchemy import inspect
from sqlalchemy.orm import Session
from collections import defaultdict

from tests.tools.db.db_setup import Base # FIXME: Change this import
from DeltaDB.types import Capture, ObjectsList
from DeltaDB.validations import validate_data, ValidateId, ValidateInstance, ValidateTablename

# List of validation rules to apply to objects
capture_validations = [ValidateId(), ValidateInstance(), ValidateTablename()]

def get_all_tables(session: Session) -> list:
    '''
    Returns instances of database tables.

    Args:
        session (Session): Active database session.

    Returns:
        list: Instances of the queried models.
    '''
    all_instances = []
    mappers = Base.registry.mappers

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

    metadata: Capture = defaultdict(dict)
    
    for obj in objects:
        inspected_obj = inspect(obj)

        for column in inspected_obj.mapper.columns:
            column_name = column.key
            column_value = getattr(obj, column_name)

            key = f'{column_name} (FK)' if column.foreign_keys else column_name
            metadata[obj.__tablename__, obj.id][key] = column_value

    return dict(metadata)


def capture_all_tables(session: Session, page_size: int = 1000) -> Capture:
    '''
    Returns a dictionary where each key is a tuple (__tablename__, id)
    and the value is a dictionary containing the table's metadata. 
    The keys are column names, and the values are their respective values in the object.
    Uses pagination to process large tables efficiently.

    Args:
        session (Session): Active database session.
        page_size (int): Number of records per page to fetch. Defaults to 1000.

    Returns:
        Capture: A dictionary with metadata for the captured objects.
    '''
    mappers = Base.registry.mappers
    metadata: Capture = defaultdict(dict)

    for mapper in mappers:
        offset = 0
        while True:
            instances = session.query(mapper.class_).limit(page_size).offset(offset).all()
            
            if not instances:
                break

            for obj in instances:
                for column in mapper.columns:
                    column_name = column.key
                    column_value = getattr(obj, column_name)

                    key = f'{column_name} (FK)' if column.foreign_keys else column_name
                    metadata[obj.__tablename__, obj.id][key] = column_value

            offset += page_size

    return dict(metadata)
