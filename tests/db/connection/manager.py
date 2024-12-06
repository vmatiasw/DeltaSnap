def get_db_connection(db_source):
    adapter_func = ADAPTERS.get(db_source)
    return adapter_func(db_source)


def __get_db_connection_adapter(db_source):
    from tests.db.connection.adapters.SqlAlchemyDBConnectionAdapter import (
        SqlAlchemyDBConnectionAdapter,
    )

    return SqlAlchemyDBConnectionAdapter(db_source)


ADAPTERS = {"sqlalchemy": __get_db_connection_adapter}
