from typing import Literal, Optional, Any

from DeltaDB.presentation.utils.validations import validate_db_type, validate_db_orm
from DeltaDB.infrastructure.adapters.DBMetadata.manager import get_db_metadata_adapter


class DBConfig:
    """
    Class for configuring which database and ORM to use and passing the corresponding dependencies.

    Args:
        db_type (Literal['sqlite', 'mysql', 'postgresql']): The type of the database.
        db_orm (Literal['sqlalchemy']): The ORM to use.
        repository (Optional[Any]): The repository instance for database interaction (default is None).
        base (Optional[Any]): The base class for model mapping (e.g., `DeclarativeBase` in SQLAlchemy, default is None).

    Raises:
        ValueError: If db_type or db_orm is not supported.

    Attributes:
        db_type (str): The type of the database.
        db_orm (str): The ORM used for database interaction.
        repository (Optional[Any]): The repository instance.
        base (Optional[Any]): The base class used for mapping.
    """

    def __init__(
        self,
        db_type: Literal["sqlite", "mysql", "postgresql"],
        db_orm: Literal["sqlalchemy"],
        repository: Optional[Any] = None,
        base: Optional[Any] = None,
    ):
        validate_db_type(db_type)
        validate_db_orm(db_orm)
        self.db_type = db_type
        self.db_orm = db_orm
        self.repository = repository
        self.base = base

    def get_db_metadata_adapter(self):
        """
        Returns the DBMetadataAdapter based on the configuration.

        This method acts as a bridge between the configuration and the
        infrastructure layer, enabling database metadata retrieval to the
        data ingestion.
        """
        return get_db_metadata_adapter(self)

    def __str__(self) -> str:
        """
        Returns a string representation of the current configuration.

        Returns:
            str: A human-readable string describing the configuration.
        """
        return f"DBConfig(db_type={self.db_type}, db_orm={self.db_orm})"
