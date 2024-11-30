from DeltaDB.config import ORM
def __get_db_transaction_adapter_class():
    match ORM:
        case "sqlalchemy":
            from tests.db.DBTransaction.SqlAlchemyDBTransactionAdapter import SqlAlchemyDBTransactionAdapter
            return SqlAlchemyDBTransactionAdapter
        case "django":
            from tests.db.DBTransaction.DjangoDBTransactionAdapter import DjangoDBTransactionAdapter
            return DjangoDBTransactionAdapter
        case _:
            raise Exception(f"ORM {ORM} not supported")

DBTransaction = __get_db_transaction_adapter_class()