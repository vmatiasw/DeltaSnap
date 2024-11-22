from abc import ABC, abstractmethod
from typing import List
from DeltaDB.types import ObjectsList, BaseModel

# Abstract base class for validations
class Validation(ABC):
    @abstractmethod
    def validate(self, data: ObjectsList):
        """Validates a list of objects.

        Args:
            data (ObjectsList): List of objects to validate.
        """
        pass

def validate_data(objects: ObjectsList, validations: List[Validation]):
    """Applies a list of validations to a list of objects.

    Args:
        objects (ObjectsList): List of objects to validate.
        validations (List[Validation]): List of validation rules.

    Raises:
        ValueError: If any validation fails.
    """
    for validation in validations:
        validation.validate(objects)

class ValidateTablename(Validation):
    def validate(self, objects: ObjectsList):
        """Validates that all objects have the '__tablename__' attribute.

        Args:
            objects (ObjectsList): List of objects to validate.

        Raises:
            ValueError: If any object lacks the '__tablename__' attribute.
        """
        if not all(hasattr(obj, '__tablename__') for obj in objects):
            raise ValueError("All objects must have the '__tablename__' attribute.")

class ValidateId(Validation):
    def validate(self, objects: ObjectsList):
        """Validates that all objects have the 'id' attribute.

        Args:
            objects (ObjectsList): List of objects to validate.

        Raises:
            ValueError: If any object lacks the 'id' attribute.
        """
        if not all(hasattr(obj, 'id') for obj in objects):
            raise ValueError("All objects must have an 'id' attribute.")

class ValidateInstance(Validation):
    def validate(self, objects: ObjectsList):
        """Validates that all objects are instances of the BaseModel type.

        Args:
            objects (ObjectsList): List of objects to validate.

        Raises:
            ValueError: If any object is not an instance of BaseModel.
        """
        if not all(isinstance(obj, BaseModel) for obj in objects):
            raise ValueError("All objects must be instances of the specified BaseModel.")