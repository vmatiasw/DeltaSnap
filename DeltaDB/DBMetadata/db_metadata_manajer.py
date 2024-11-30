from DeltaDB.config import ORM, APP_LABEL
from tests.db.DBConnection.db_connection_manajer import db_connection

def __get_db_metadata_adapter():
    match ORM:
        case "sqlalchemy":
            from DeltaDB.DBMetadata.DBMetadataAdapters.SQLAlchemyMetadataAdapter import SQLAlchemyMetadataAdapter
            return SQLAlchemyMetadataAdapter(db_connection.get_base())
        case "django":
            from DeltaDB.DBMetadata.DBMetadataAdapters.DjangoMetadataAdapter import DjangoMetadataAdapter
            return DjangoMetadataAdapter(APP_LABEL)
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_metadata = __get_db_metadata_adapter()