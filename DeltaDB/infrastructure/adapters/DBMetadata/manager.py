def _get_db_metadata_adapter(db_config):
    """
    Retrieves the appropriate metadata adapter based on the ORM configured in DBConfig.

    Args:
        db_config: An instance of DBConfig.

    Returns:
        An ORM/DB-specific metadata adapter.

    Raises:
        ValueError: If the ORM/DB configured in DBConfig is not supported.
    """
    adapter_func = ADAPTERS.get(db_config.db_source)
    if not adapter_func:
        raise ValueError(
            f"Unsupported ORM/DB '{db_config.db_source}'. "
            f"Available ORM/DB: {list(ADAPTERS.keys())}."
        )
    return adapter_func(db_config)


def __get_sqlalchemy_adapter(db_config):
    """
    Retrieves the adapter for SQLAlchemy metadata.

    Args:
        db_config: An instance of DBConfig containing `base` (a subclass of DeclarativeBase)
                  and `test_session` (Session).

    Returns:
        SQLAlchemyMetadataAdapter: Adapter for interacting with SQLAlchemy metadata.

    Raises:
        ValueError: If `base` is not a subclass of DeclarativeBase or `test_session` is not a Session.
    """
    from sqlalchemy.orm import DeclarativeBase, Session
    from DeltaDB.infrastructure.adapters.DBMetadata.SQLAlchemyMetadataAdapter import (
        SQLAlchemyMetadataAdapter,
    )

    if not issubclass(db_config.base, DeclarativeBase) or not isinstance(
        db_config.test_session, Session
    ):
        raise ValueError(
            "You must provide `base` (a subclass of DeclarativeBase) and a `test_session` (Session) for SQLAlchemy."
        )

    return SQLAlchemyMetadataAdapter(db_config.base, db_config.test_session)


ADAPTERS = {"sqlalchemy": __get_sqlalchemy_adapter}
