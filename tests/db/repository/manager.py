def get_repository(db_connection):
    adapter_func = ADAPTERS.get(db_connection.db_source)
    assert (
        adapter_func
    ), f"ORM/DB {db_connection.db_source} repository adapter is not implemented"

    return adapter_func(db_connection)


def __get_sqlalchemy_adapter(db_connection):
    from tests.db.repository.adapters.SqlAlchemyRepository import SqlAlchemyRepository

    return SqlAlchemyRepository(db_connection.base)


def __get_django_adapter(db_connection):
    from tests.db.repository.adapters.DjangoRepository import DjangoRepository

    return DjangoRepository(db_connection.base)


ADAPTERS = {"sqlalchemy": __get_sqlalchemy_adapter, "django": __get_django_adapter}
