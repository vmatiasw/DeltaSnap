from DeltaDB.config import ORM

def __get_db_metadata_adapter():
    match ORM:
        case "sqlalchemy":
            from DeltaDB.DBMetadata.SQLAlchemyMetadataAdapter import SQLAlchemyMetadataAdapter
            return SQLAlchemyMetadataAdapter()
        case "django":
            from DeltaDB.DBMetadata.DjangoMetadataAdapter import DjangoMetadataAdapter
            return DjangoMetadataAdapter()
        case _:
            raise Exception(f"ORM {ORM} not supported")

db_metadata = __get_db_metadata_adapter()