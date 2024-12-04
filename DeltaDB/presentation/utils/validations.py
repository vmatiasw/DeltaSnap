# Configuration constants
DBS_SUPPORTED = {"sqlite", "mysql", "postgresql"}
"""Set of supported database types."""

ORMS_SUPPORTED = {"sqlalchemy"}
"""Set of supported ORMs."""


def validate_db_type(db_type: str) -> None:
    if db_type not in DBS_SUPPORTED:
        raise ValueError(
            f"Invalid database type '{db_type}'. " f"Valid options: {DBS_SUPPORTED}."
        )


def validate_db_orm(db_orm: str) -> None:
    if db_orm not in ORMS_SUPPORTED:
        raise ValueError(
            f"Invalid ORM '{db_orm}'. " f"Valid options: {ORMS_SUPPORTED}."
        )
