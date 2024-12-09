import django
from django.conf import settings
from django.db import connections, transaction
from django.db.utils import OperationalError
from contextlib import contextmanager

from tests.db.connection.IDBConnection import IDBConnection
from tests.db.config import APP_LABEL, DB_PATH


class DjangoDBConnectionAdapter(IDBConnection):
    def __init__(self, db_source: str) -> None:
        """
        Inicializa la configuración de la base de datos y Django.
        """
        super().__init__()
        self.db_source = db_source
        self._configure_django()
        from tests.db.game_test.models.django import Base

        self.base = Base

    def _configure_django(self) -> None:
        """
        Configura los ajustes mínimos de Django para usar su ORM.
        """
        databases = {
            "sqlite": "sqlite3",
            "postgresql": "postgresql",
            "mysql": "mysql",
        }
        settings.configure(
            DEBUG=True,
            DATABASES={
                "default": {
                    "ENGINE": f"django.db.backends.{databases[self.database]}",
                    "NAME": DB_PATH,
                }
            },
            INSTALLED_APPS=["django.contrib.contenttypes", APP_LABEL],
            MIDDLEWARE=[],
            ROOT_URLCONF="__main__",
        )
        django.setup()

    def create_tables(self) -> None:
        """
        Crea las tablas en la base de datos usando las migraciones.
        :param models_module: Módulo que contiene los modelos.
        """
        models_module = django.apps.apps.get_models()
        with connections["default"].schema_editor() as schema_editor:
            for model in models_module:
                schema_editor.create_model(model)

    def drop_tables(self) -> None:
        """
        Elimina las tablas de la base de datos.
        :param models_module: Módulo que contiene los modelos.
        """
        models_module = django.apps.apps.get_models()
        with connections["default"].schema_editor() as schema_editor:
            for model in reversed(models_module):
                if self._table_exists(model._meta.db_table):
                    schema_editor.delete_model(model)

    @staticmethod
    def _table_exists(table_name: str) -> bool:
        """
        Verifica si una tabla existe en la base de datos.
        """
        cursor = connections["default"].cursor()
        try:
            cursor.execute(
                f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
            )
            return cursor.fetchone() is not None
        except OperationalError:
            return False

    @staticmethod
    @contextmanager
    def new_test_transaction():
        """
        Un administrador de contexto para manejar transacciones en modo de prueba.
        """
        with transaction.atomic():
            yield None
            transaction.set_rollback(True)

    def get_base(self):
        """
        Devuelve la base de los modelos de Django.
        """
        return self.base
