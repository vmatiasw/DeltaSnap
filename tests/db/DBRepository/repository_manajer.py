from DeltaDB.config import ORM
from tests.db.DBConnection.db_connection_manajer import db_connection

def __get_repository():
    match ORM:
        case "sqlalchemy":
            from tests.db.DBRepository.SqlAlchemyRepository import SqlAlchemyRepository
            return SqlAlchemyRepository(db_connection.get_base())
        case _:
            raise Exception(f"ORM {ORM} not supported")

repository = __get_repository()