from typing import Literal

from src.validations import validate_db_type, validate_db_orm
from src.domain.data_processing.ingestion import capture_all_records
from src.domain.data_processing.analysis import diff_records_captures
from src.DBMetadata.manajer import get_db_metadata_adapter


class DeltaDB:
    """
    Main class for database and ORM interaction.

    This class provides an abstraction for configuring and interacting with
    databases compatible with specified types and ORMs. It includes methods for
    capturing and comparing data within the database.

    Args:
        db_type (Literal['sqlite', 'mysql', 'postgresql']): The database type.
        db_orm (Literal['sqlalchemy']): The ORM to be used.
        repository (optional): A repository instance to interact with the database.
        base (optional): A base class for model mapping (e.g., `declarative_base` in SQLAlchemy).

    Raises:
        ValueError: If `db_type` or `db_orm` are not valid.

    Attributes:
        db_type (str): Configured database type.
        db_orm (str): Configured ORM.
        repository (object): The repository provided by the user.
        base (object): The base class for model mapping.
        db_metadata (object): The configured database metadata adapter.
    """

    def __init__(
        self,
        db_type: Literal["sqlite", "mysql", "postgresql"],
        db_orm: Literal["sqlalchemy"],
        repository=None,
        base=None,
    ) -> None:
        """
        Initializes a DeltaDB instance with the specified configuration.
        """
        validate_db_type(db_type)
        validate_db_orm(db_orm)
        self.db_type = db_type
        self.db_orm = db_orm
        self.repository = repository
        self.base = base
        self.db_metadata = get_db_metadata_adapter(self)

    def __str__(self) -> str:
        """
        Returns a string representation of the current configuration.

        Returns:
            str: A human-readable string describing the configuration.
        """
        return f"DeltaDB(db_type={self.db_type}, db_orm={self.db_orm})"

    def capture_all_records(self):  # FIXME: es records
        """
        Captures the structure and data of all tables in the database.

        Returns:
            object: The result of the capture processed by the adapter.
        """
        return capture_all_records(self.db_metadata)

    @staticmethod
    def diff_records_captures(initial_capture, final_capture):
        """
        Compares two data captures and returns the differences.

        Args:
            initial_capture (object): The initial data capture.
            final_capture (object): The final data capture.

        Returns:
            object: The result of the capture comparison.
        """
        return diff_records_captures(initial_capture, final_capture)
