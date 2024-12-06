from typing import Literal, Optional, Any
from dataclasses import dataclass

from DeltaDB.infrastructure.adapters.DBMetadata.manager import _get_db_metadata_adapter


@dataclass
class DBConfig:
    """
    Class for configuring which database and ORM to use, and passing the corresponding dependencies.
    """

    db_type: Literal["sqlite", "mysql", "postgresql"]
    db_orm: Literal["sqlalchemy"]
    test_session: Optional[Any] = None
    base: Optional[Any] = None

    def _get_db_metadata_adapter(self):
        """
        Returns the DBMetadataAdapter based on the configuration.

        This method acts as a bridge between the configuration and the
        infrastructure layer, enabling database metadata retrieval to the
        data ingestion.
        """
        return _get_db_metadata_adapter(self)
