from DeltaDB.config import ORM
from DeltaDB.config import APP_LABEL

def __get_db_connection_adapter():
    match ORM:
        case "sqlalchemy":
            from DeltaDB.DBConnection.SqlAlchemyDBConnectionAdapter import SqlAlchemyDBConnectionAdapter
            return SqlAlchemyDBConnectionAdapter()
        case "django":
            from DeltaDB.DBConnection.DjangoDBConnectionAdapter import DjangoDBConnectionAdapter
            return DjangoDBConnectionAdapter(APP_LABEL)
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_connection= __get_db_connection_adapter()