ORM = "sqlalchemy" # "django" | "sqlalchemy"

def __get_db_manager():
    match ORM:
        case "sqlalchemy":
            from tests.tools.db.DBConnectionAdapters.SqlAlchemyDBConnectionAdapter import SqlAlchemyDBConnectionAdapter
            return SqlAlchemyDBConnectionAdapter()
        case "django":
            from tests.tools.db.DBConnectionAdapters.DjangoDBConnectionAdapter import DjangoDBConnectionAdapter
            return DjangoDBConnectionAdapter()
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_connection_adapter= __get_db_manager()

def __get_db_metedata_adapter():
    match ORM:
        case "sqlalchemy":
            from tests.tools.db.DBMetadataAdapters.SQLAlchemyMetadataAdapter import SQLAlchemyMetadataAdapter
            return SQLAlchemyMetadataAdapter()
        case "django":
            from tests.tools.db.DBMetadataAdapters.DjangoMetadataAdapter import DjangoMetadataAdapter
            return DjangoMetadataAdapter()
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_metedata_adapter = __get_db_metedata_adapter()