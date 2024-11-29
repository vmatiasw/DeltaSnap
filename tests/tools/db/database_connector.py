ORM = "sqlalchemy" # "django" | "sqlalchemy"

def __get_db_manager():
    match ORM:
        case "sqlalchemy":
            from tests.tools.db.DBManajers.SQLAlchamyDBManager import SqlAlchemyDBManager
            return SqlAlchemyDBManager()
        case "django":
            pass
            # from tests.tools.db.DBManajers.DjangoDBManager import DjangoDBManager
            # return DjangoDBManager(DATABASE_NAME)
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_manajer = __get_db_manager()

def __get_orm_adapter():
    match ORM:
        case "sqlalchemy":
            from tests.tools.db.ORMAdapters.SQLAlchemyAdapter import SQLAlchemyAdapter
            return SQLAlchemyAdapter()
        case "django":
            pass
        case _:
            raise Exception(f"ORM {ORM} not supported")

orm_adapter = __get_orm_adapter()