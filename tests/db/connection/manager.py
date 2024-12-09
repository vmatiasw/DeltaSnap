def get_db_connection(db_source):
    adapter_func = ADAPTERS.get(db_source)
    assert adapter_func, f"ORM/DB {db_source} connection adapter is not implemented"

    return adapter_func(db_source)


def __get_sqlalchemy_adapter(db_source):
    from tests.db.connection.adapters.SqlAlchemyDBConnectionAdapter import (
        SqlAlchemyDBConnectionAdapter,
    )

    return SqlAlchemyDBConnectionAdapter(db_source)


def __get_django_adapter(db_source):
    from tests.db.connection.adapters.DjangoDBConnectionAdapter import (
        DjangoDBConnectionAdapter,
    )

    return DjangoDBConnectionAdapter(db_source)


ADAPTERS = {"sqlalchemy": __get_sqlalchemy_adapter, "django": __get_django_adapter}
