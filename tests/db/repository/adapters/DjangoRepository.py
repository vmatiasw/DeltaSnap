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
        """Crea una instancia de un modelo de base de datos."""
        model_class = self.get_model_by_name(model_name)
        instance = model_class(**kwargs)
        instance.save()
        return instance

    def add(self, instance: Any) -> None:
        """Añade una instancia a la sesión de la base de datos."""
        instance.save()

    def get(self, model_name: str, id: int) -> Any:
        """Obtiene un registro de la base de datos dado un modelo y un id."""
        model_class = self.get_model_by_name(model_name)
        return model_class.objects.get(id=id)

    def query(self, model: Type[Any]) -> Any:
        """Realiza una consulta a la base de datos para un modelo específico."""
        return model.objects.all()

    def filter(self, model: Type[Any], **kwargs: Any) -> Any:
        """Filtra una consulta de base de datos usando los parámetros proporcionados."""
        return model.objects.filter(**kwargs)

    def get_model_by_name(self, model_name: str) -> Type[Model]:
        """
        Obtiene un modelo de base de datos por su nombre.
        """
        model = apps.get_model(APP_LABEL + "." + model_name)
        return model

    def commit(self) -> None:
        """Hace commit a la sesión de la base de datos."""
        pass

    def flush(self, objects = []) -> None:
        """Hace flush a la sesión de la base de datos"""
        for obj in objects:
            obj.save()

    def append(self, list, instance: Any) -> None:
        """Añade una instancia a la sesión de la base de datos."""
        list.add(instance)
        
    def count(self, list) -> int:
        return list.count()
    
    def get_list(self, list) -> list:
        return list.all()

    def get_key(self, instance) -> int:
        return instance