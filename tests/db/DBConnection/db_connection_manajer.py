from DeltaDB.config import ORM
def __get_db_connection_adapter():
    match ORM:
        case "sqlalchemy":
            from tests.db.DBConnection.SqlAlchemyDBConnectionAdapter import SqlAlchemyDBConnectionAdapter
            return SqlAlchemyDBConnectionAdapter()
        case "django":
            from tests.db.DBConnection.DjangoDBConnectionAdapter import DjangoDBConnectionAdapter
            return DjangoDBConnectionAdapter()
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_connection= __get_db_connection_adapter()