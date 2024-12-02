
from typing import Literal

from src.domain.data_processing.ingestion import capture_all_tables
from src.domain.data_processing.analysis import diff_captures

DBS_SUPPORTED = {'sqlite', 'mysql', 'postgresql'}
ORMS_SUPPORTED = {'sqlalchemy'}

def DeltaDB_setup(
    db_type: Literal['sqlite', 'mysql' ,'postgresql'],
    db_orm : Literal['sqlalchemy'],
    repository = None,
    base = None):
    return DeltaDB(db_type, db_orm, repository=repository, base=base)

class DeltaDB:
    def __init__(self, db_type, db_orm, repository = None, base = None) -> None:
        self.__check_types(db_type, db_orm)
        self.db_type = db_type
        self.db_orm = db_orm
        self.base = base
        self.repository = repository
        self.db_metadata = self.__get_db_metadata_adapter()
    
    def __str__(self):
        return f"DatabaseConfig(db_type={self.db_type}, db_orm={self.db_orm})"
    
    def __get_db_metadata_adapter(self):
        match self.db_orm:
            case "sqlalchemy":
                if self.base is None or self.repository is None:
                    raise ValueError("Debe pasar una instancia de base y repository")
                from src.adapters.DBMetadata.SQLAlchemyMetadataAdapter import SQLAlchemyMetadataAdapter
                return SQLAlchemyMetadataAdapter(self.base, self.repository)
            case _:
                raise Exception(f"ORM {self.db_orm} not supported")
            
    def capture_all_tables(self):
        return capture_all_tables(self.db_metadata)
    
    @staticmethod
    def diff_captures(initial_capture, final_capture):
        return diff_captures(initial_capture, final_capture)

    def put_db_type(self, db_type:Literal['sqlite', 'mysql' ,'postgresql']) -> None:
        self.db_type = db_type
        
    def put_db_orm(self, db_orm:Literal['sqlalchemy']) -> None:
        self.db_orm = db_orm
        
    def __check_types(self, db_type, db_orm):
        if db_type not in DBS_SUPPORTED:
            raise ValueError(f"Tipo de base de datos '{db_type}' no válido. Valores válidos: {DBS_SUPPORTED}")
        if db_orm not in ORMS_SUPPORTED:
            raise ValueError(f"ORM '{db_orm}' no válido. Valores válidos: {ORMS_SUPPORTED}")