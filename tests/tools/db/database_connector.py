ORM = "sqlalchemy" # "django" | "sqlalchemy"

def __get_db_manager():
    match ORM:
        case "sqlalchemy":
            from tests.tools.db.DBManajers.SQLAlchamyDBManager import SqlAlchemyDBManager
            return SqlAlchemyDBManager()
        case "django":
            from tests.tools.db.DBManajers.DjangoDBManager import DjangoDBManager
            return DjangoDBManager()
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_manajer = __get_db_manager()

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