from DeltaDB.config import ORM, APP_LABEL
from DeltaDB.DBConnection.db_connection_manajer import db_connection
from DeltaDB.DBRepository.repository_manajer import repository

def __get_db_metadata_adapter():
    match ORM:
        case "sqlalchemy":
            from DeltaDB.DBMetadata.DBMetadataAdapters.SQLAlchemyMetadataAdapter import SQLAlchemyMetadataAdapter
            return SQLAlchemyMetadataAdapter(db_connection.get_base(), repository)
        case "django":
            from DeltaDB.DBMetadata.DBMetadataAdapters.DjangoMetadataAdapter import DjangoMetadataAdapter
            return DjangoMetadataAdapter(APP_LABEL)
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_metadata = __get_db_metadata_adapter()