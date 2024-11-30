from DeltaDB.config import ORM
from tests.db.DBConnection.db_connection_manajer import db_connection

def __get_db_metadata_adapter():
    match ORM:
        case "sqlalchemy":
            from DeltaDB.DBMetadata.SQLAlchemyMetadataAdapter import SQLAlchemyMetadataAdapter
            return SQLAlchemyMetadataAdapter(db_connection.get_base())
        case "django":
            from DeltaDB.DBMetadata.DjangoMetadataAdapter import DjangoMetadataAdapter
            return DjangoMetadataAdapter(db_connection.get_base())
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_metadata = __get_db_metadata_adapter()