from typing import Any, Type
from django.db import models, transaction
from django.apps import apps

from tests.db.DBTransaction.DBTransactionAdapter import DBTransactionAdapter
from DeltaDB.config import APP_LABEL

class DjangoDBTransactionAdapter(DBTransactionAdapter):
    def __init__(self, db_session: Any) -> None:
        """
        Inicializa el adaptador. En Django, no necesitamos un `db_session`,
        pero se mantiene para compatibilidad.
        """
        super().__init__(db_session)
        self.app_label = APP_LABEL
        
    def get_model_by_name(self, model_name: str) -> type[models.Model]:
        """Devuelve la clase de modelo (tabla) por su nombre."""
        return apps.get_model(self.app_label + "." + model_name)

    def instance_model(self, model_name: str, **kwargs: Any) -> Any:
        """
        Crea una instancia de un modelo Django.

        Args:
            model_name (str): Nombre del modelo (registrado en la base de datos).
            kwargs (Any): Campos del modelo con valores iniciales.

        Returns:
            Una instancia del modelo sin guardar.
        """
        model_class = self.get_model_by_name(model_name)
        return model_class(**kwargs)

    def add(self, instance: models.Model) -> None:
        """
        Guarda una instancia del modelo en la base de datos.

        Args:
            instance (models.Model): Instancia del modelo.
        """
        instance.save()

    def commit(self) -> None:
        """
        Django maneja automáticamente las transacciones, pero puedes
        usarlo explícitamente con `transaction.commit`.
        """
        transaction.commit()

    def flush(self) -> None:
        """
        Django no tiene un método directo equivalente a `flush`,
        ya que las operaciones se manejan directamente en la base de datos.
        """
        raise NotImplementedError("Flush no es necesario en Django.")

    def get(self, model_name: str, id: int) -> Any:
        """
        Obtiene un registro de la base de datos dado un modelo y un ID.

        Args:
            model_name (str): Nombre del modelo.
            id (int): ID del registro.

        Returns:
            El objeto del modelo correspondiente al ID.
        """
        model_class = self.get_model_by_name(model_name)
        return model_class.objects.get(id=id)

    def query(self, model: str | Type[Any]) -> models.QuerySet:
        """
        Realiza una consulta a la base de datos para un modelo específico.

        Args:
            model (str | Type[Any]): Nombre o clase del modelo.

        Returns:
            Un QuerySet de Django para el modelo.
        """
        if isinstance(model, str):
            model = self.get_model_by_name(model)
        return model.objects.all()

    def filter(self, query: models.QuerySet, *args: Any, **kwargs: Any) -> models.QuerySet:
        """
        Filtra una consulta de base de datos usando los parámetros proporcionados.

        Args:
            query (models.QuerySet): QuerySet inicial.
            args (Any): Argumentos posicionales de filtros.
            kwargs (Any): Argumentos con nombre para filtros.

        Returns:
            Un QuerySet filtrado.
        """
        return query.filter(*args, **kwargs)
