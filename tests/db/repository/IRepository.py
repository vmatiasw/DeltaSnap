from typing import Any, Protocol, Type


class IRepository(Protocol):

    def instance_model(self, model_name: str, **kwargs: Any) -> Any:
        """Crea una instancia de un modelo de base de datos."""
        ...

    def add(self, instance: Any) -> None:
        """Añade una instancia a la sesión de la base de datos."""
        ...

    def get(self, model_name: str, id: int) -> Any:
        """Obtiene un registro de la base de datos dado un modelo y un id."""
        ...

    def query(self, model: str | Type[Any]) -> Any:
        """
        Realiza una consulta a la base de datos para un modelo específico.

        Args:
            model (str | Type[Any]): El nombre del modelo o la clase del modelo.
        """
        ...

    def filter(self, query, *args: Any, **kwargs: Any) -> Any:
        """Filtra una consulta de base de datos usando los parámetros proporcionados."""
        ...

    def get_model_by_name(self, model_name: str) -> Any:
        """Obtiene un modelo de base de datos por su nombre."""
        ...

    def commit(self) -> None:
        """Hace commit a la sesión de la base de datos."""
        ...

    def flush(self) -> None:
        """
        Hace flush a la sesión de la base de datos.
        Y expira todos los objetos de la sesión.
        """
        ...

    def append(self, list, instance) -> None:
        """
        Agrega `instance` a `list`.
        """
        ...
        
    def get_list(self, list) -> list:
        ...
        
    def count(self, list) -> int:
        ...