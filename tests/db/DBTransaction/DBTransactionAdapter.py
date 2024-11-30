from abc import ABC, abstractmethod
from typing import Any


class DBTransactionAdapter(ABC):
    def __init__(self, db_session: Any) -> None:
        """Inicializa el adaptador con una sesión de base de datos."""
        self.session: Any = db_session

    @abstractmethod
    def instance_model(self, model_name:str, **kwargs: Any) -> Any:
        """Crea una instancia de un modelo de base de datos."""
        pass
    
    @abstractmethod
    def add(self, instance: Any) -> None:
        """Añade una instancia a la sesión de la base de datos."""
        pass

    @abstractmethod
    def commit(self) -> None:
        """Hace commit a la sesión de la base de datos."""
        pass

    @abstractmethod
    def flush(self) -> None:
        """Hace flush a la sesión de la base de datos."""
        pass

    @abstractmethod
    def get(self, model_name: str, id: int) -> Any:
        """Obtiene un registro de la base de datos dado un modelo y un id."""
        pass

    @abstractmethod
    def query(self, model_name: str) -> Any:
        """Realiza una consulta a la base de datos para un modelo específico."""
        pass

    @abstractmethod
    def filter(self, query, *args: Any, **kwargs: Any) -> Any:
        """Filtra una consulta de base de datos usando los parámetros proporcionados."""
        pass
