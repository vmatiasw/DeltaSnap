
def __get_sqlalchemy_adapter(delta_db):
    """
    Retrieves the adapter for SQLAlchemy metadata.

    Args:
        delta_db: An instance of DeltaDB containing `base` (a subclass of DeclarativeBase) 
                  and `repository` (an implementation of IRepository).

    Returns:
        SQLAlchemyMetadataAdapter: Adapter for interacting with SQLAlchemy metadata.

    Raises:
        ValueError: If `base` is not a subclass of DeclarativeBase or `repository` does not implement IRepository.
    """
    from sqlalchemy.orm import DeclarativeBase
    from src.DBMetadata.adapters.SQLAlchemyMetadataAdapter import SQLAlchemyMetadataAdapter, IRepository

    if not issubclass(delta_db.base, DeclarativeBase) or not isinstance(delta_db.repository, IRepository):
        raise ValueError(
            "You must provide `base` (a subclass of DeclarativeBase) and a `repository` (implementing IRepository) for SQLAlchemy."
        )
    return SQLAlchemyMetadataAdapter(delta_db.base, delta_db.repository)


ADAPTERS = {
    "sqlalchemy": __get_sqlalchemy_adapter
}


def get_db_metadata_adapter(delta_db):
    """
    Retrieves the appropriate metadata adapter based on the ORM configured in DeltaDB.

    Args:
        delta_db: An instance of DeltaDB.

    Returns:
        An ORM-specific metadata adapter.

    Raises:
        ValueError: If the ORM configured in DeltaDB is not supported.
    """
    adapter_func = ADAPTERS.get(delta_db.db_orm)
    if not adapter_func:
        raise ValueError(
            f"Unsupported ORM '{delta_db.db_orm}'. "
            f"Available ORMs: {list(ADAPTERS.keys())}."
        )
    return adapter_func(delta_db)
