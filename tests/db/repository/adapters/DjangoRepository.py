from typing import Any, Type
from django.db import transaction
from django.db.models import Model
from django.apps import apps

from tests.db.game_test.models.django import Base
from tests.db.config import APP_LABEL


class DjangoRepository:
    def __init__(self, base: Base) -> None:
        self.base = base

    def instance_model(self, model_name: str, **kwargs: Any) -> Any:
        """Creates an instance of a database model."""
        model_class = self.get_model_by_name(model_name)
        instance = model_class(**kwargs)
        instance.save()
        return instance

    def add(self, instance: Any) -> None:
        """Adds an instance to the database session."""
        instance.save()

    def get(self, model_name: str, id: int) -> Any:
        """Retrieves a record from the database given a model and an ID."""
        model_class = self.get_model_by_name(model_name)
        return model_class.objects.get(id=id)

    def query(self, model: Type[Any]) -> Any:
        """Performs a query on the database for a specific model."""
        return model.objects.all()

    def filter(self, model: Type[Any], **kwargs: Any) -> Any:
        """Filters a database query using the provided parameters."""
        return model.objects.filter(**kwargs)

    def get_model_by_name(self, model_name: str) -> Type[Model]:
        """
        Retrieves a database model by its name.
        """
        model = apps.get_model(f"{APP_LABEL}.{model_name}")
        return model

    def commit(self) -> None:
        """Commits the database session (no-op in Django ORM)."""
        pass

    def flush(self, objects: list = []) -> None:
        """Flushes the database session by saving the provided objects."""
        for obj in objects:
            obj.save()

    def append(self, list, instance: Any) -> None:
        """Adds an instance to a list in the session."""
        list.add(instance)

    def count(self, list) -> int:
        """Returns the count of items in the provided list."""
        return list.count()

    def get_list(self, list) -> list:
        """Returns all items in the provided list."""
        return list.all()

    def get_key(self, instance) -> int:
        """Returns the primary key (ID) of the given instance."""
        return instance
