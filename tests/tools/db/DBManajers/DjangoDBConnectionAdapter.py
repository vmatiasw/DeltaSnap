import django
from django.db import models, transaction
from django.conf import settings
from django.core.management import call_command

from tests.tools.db.DBManajers.DBConnectionAdapter import DBConnectionAdapter

class DjangoDBConnectionAdapter(DBConnectionAdapter):
    def __init__(self):
        super().__init__()
        self._setup_django()
        
    def _get_engine(self) -> str:
        """Devuelve el motor de la base de datos."""
        match self.database:
            case 'sqlite':
                return 'sqlite3'
            case 'mysql':
                return 'mysql'
            case 'postgresql':
                return 'postgresql'
            case _:
                raise Exception(f"Database {self.database} not supported")

    def _setup_django(self):
        """Configura el entorno de Django para la base de datos seleccionada."""
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': f'django.db.backends.{self._get_engine()}',
                    'NAME': self.db_name,
                    'USER': self.username,
                    'PASSWORD': self.password,
                    'HOST': self.host,
                    'PORT': self.port,
                }
            }
        )
        django.setup()

    def get_base(self):
        """Devuelve la clase Base de Django (en este caso, no hay Base explícita como en SQLAlchemy)."""
        return models.Model

    def get_new_session(self):
        """
        Devuelve una sesión nueva de Django, pero en realidad, Django maneja la transacción automáticamente.
        Si se necesita un control manual, se puede usar el contexto de transacciones.
        """
        return transaction.atomic()

    def create_tables(self) -> None:
        """Crea las tablas en la base de datos utilizando Django ORM."""
        call_command('migrate')

    def drop_tables(self) -> None:
        """Elimina las tablas en la base de datos utilizando Django ORM."""
        call_command('flush', '--no-input')
