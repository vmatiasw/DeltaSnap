from typing import Any, Protocol, Type


class IRepository(Protocol):

    def instance_model(self, model_name: str, **kwargs: Any) -> Any:
        """Creates an instance of a database model."""
        ...

    def add(self, instance: Any) -> None:
        """Adds an instance to the database session."""
        ...

    def get(self, model_name: str, id: int) -> Any:
        """Retrieves a record from the database given a model and an ID."""
        ...

    def query(self, model: str | Type[Any]) -> Any:
        """
        Performs a query on the database for a specific model.

        Args:
            model (str | Type[Any]): The name or the class of the model to query.
        """
        ...

    def filter(self, query, *args: Any, **kwargs: Any) -> Any:
        """Filters a database query using the provided parameters."""
        ...

    def get_model_by_name(self, model_name: str) -> Any:
        """Retrieves a database model by its name."""
        ...

    def commit(self) -> None:
        """Commits the current database session."""
        ...

    def flush(self, objects) -> None:
        """
        Flushes the database session and expires all objects in the session.
        """
        ...

    def append(self, list, instance) -> None:
        """
        Appends `instance` to the given `list`.
        """
        ...
        
    def get_list(self, list) -> list:
        """Returns the list as is."""
        ...
        
    def count(self, list) -> int:
        """Returns the count of items in the given list."""
        ...
        
    def get_key(self, instance) -> int:
        """Returns the key (ID) of the given instance."""
        ...
