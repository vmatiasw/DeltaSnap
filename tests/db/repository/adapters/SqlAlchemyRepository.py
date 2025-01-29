from typing import Any, Type

from tests.db.connection.adapters.SqlAlchemyDBConnectionAdapter import current_session
from tests.db.game_test.models.sql_alchemy import Base


class SqlAlchemyRepository:
    def __init__(self, base: Base) -> None:
        self.base = base

    def get_model_by_name(self, model_name: str) -> Any:
        """Retrieves a database model by its name."""
        for mapper in self.base.registry.mappers:
            if model_name == mapper.class_.__name__:
                return mapper.class_

        raise ValueError(
            f"Model {model_name} not defined. \n Available models: {[mapper.class_.__name__ for mapper in self.base.registry.mappers]}"
        )

    def instance_model(self, model_name: str, **kwargs: Any) -> Any:
        """
        Creates an instance of a database model using the model name
        and the provided parameters.
        """
        model_class = self.get_model_by_name(model_name)
        if not model_class:
            raise ValueError(f"Model {model_name} not found.")

        # Validate if the model is a valid database model (it must have a table mapping)
        if not hasattr(model_class, "__table__"):
            raise ValueError(f"{model_name} is not a valid database model.")

        # Create the model instance
        instance = model_class(**kwargs)
        return instance

    def add(self, instance: Any) -> None:
        """Adds an instance to the database session."""
        current_session.get().add(instance)

    def append(self, list, instance: Any) -> None:
        """Appends an instance to the provided list."""
        list.append(instance)

    def commit(self) -> None:
        """Commits the database session."""
        current_session.get().commit()

    def flush(self, objects: list = []) -> None:
        """
        Flushes the database session.
        Also expires all objects in the session.
        """
        current_session.get().flush()
        current_session.get().expire_all()

    def get(self, model_name: str, id: int) -> Any:
        """Retrieves a record from the database given a model and an ID."""
        model = self.get_model_by_name(model_name)
        return current_session.get().get(model, id)

    def query(self, model: str | Type[Any]) -> Any:
        """
        Executes a query on the database for a specific model.

        Args:
            model (str | Type[Any]): The name or class of the model.
        """
        if isinstance(model, str):
            model = self.get_model_by_name(model)

        return current_session.get().query(model)

    def filter(self, query, *args: Any, **kwargs: Any) -> Any:
        """Filters a database query using the provided parameters."""
        return query.filter(*args, **kwargs)

    def count(self, list) -> int:
        """Returns the count of items in the provided list."""
        return len(list)

    def get_list(self, list) -> list:
        """Returns the list of items."""
        return list

    def get_key(self, instance) -> int:
        """Returns the primary key (ID) of the given instance."""
        return instance.id
