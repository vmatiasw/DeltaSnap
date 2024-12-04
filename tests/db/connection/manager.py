from tests.db.config import ORM


def __get_db_connection_adapter_class():
    match ORM:
        case "sqlalchemy":
            from tests.db.connection.adapters.SqlAlchemyDBConnectionAdapter import (
                SqlAlchemyDBConnectionAdapter,
            )

            return SqlAlchemyDBConnectionAdapter
        case _:
            raise Exception(f"ORM {ORM} not supported")


DBConnection = __get_db_connection_adapter_class()
