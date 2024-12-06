def get_repository(db_connection):
    adapter_func = ADAPTERS.get(db_connection.db_source)
    return adapter_func(db_connection)


def __get_repository_adapter(db_connection):
    from tests.db.repository.adapters.SqlAlchemyRepository import SqlAlchemyRepository

    return SqlAlchemyRepository(db_connection.base)


ADAPTERS = {"sqlalchemy": __get_repository_adapter}
