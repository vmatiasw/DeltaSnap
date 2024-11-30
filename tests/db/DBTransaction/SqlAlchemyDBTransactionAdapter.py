from typing import Any, Type

from tests.db.DBTransaction.DBTransactionAdapter import DBTransactionAdapter
from DeltaDB.DBMetadata.db_metadata_manajer import db_metadata

class SqlAlchemyDBTransactionAdapter(DBTransactionAdapter):
    
    def instance_model(self, model_name: str, **kwargs: Any) -> Any:
        """
        Crea una instancia de un modelo de base de datos usando el nombre del modelo
        y los parámetros proporcionados.
        """
        # Suponiendo que 'models' es un diccionario de clases de modelos disponibles
        model_class = db_metadata.get_model_by_name(model_name)
        if not model_class:
            raise ValueError(f"El modelo {model_name} no se encuentra definido.")
        
        # Validar que el modelo tenga un mapeo de clases (es un modelo de base de datos)
        if not hasattr(model_class, "__table__"):
            raise ValueError(f"{model_name} no es un modelo de base de datos válido.")
        
        # Crear la instancia del modelo
        instance = model_class(**kwargs)
        return instance
    
    def add(self, instance: Any) -> None:
        """Añade una instancia a la sesión de la base de datos."""
        self.session.add(instance)

    def commit(self) -> None:
        """Hace commit a la sesión de la base de datos."""
        self.session.commit()

    def flush(self) -> None:
        """
        Hace flush a la sesión de la base de datos.
        Y expira todos los objetos de la sesión.
        """
        self.session.flush()
        self.session.expire_all()

    def get(self, model_name: str, id: int) -> Any:
        """Obtiene un registro de la base de datos dado un modelo y un id."""
        model = db_metadata.get_model_by_name(model_name)
        return self.session.get(model, id)

    def query(self, model: str | Type[Any]) -> Any:
        """
        Realiza una consulta a la base de datos para un modelo específico.
        
        Args:
            model (str | Type[Any]): El nombre del modelo o la clase del modelo.
        """
        if isinstance(model, str):
            model = db_metadata.get_model_by_name(model)
        
        return self.session.query(model)

    def filter(self, query, *args: Any, **kwargs: Any) -> Any:
        """Filtra una consulta de base de datos usando los parámetros proporcionados."""
        return query.filter(*args, **kwargs)
