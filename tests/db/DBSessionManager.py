from typing import Any
from contextvars import ContextVar

from tests.db.DBConnection.db_connection_manajer import db_connection

# ContextVar para almacenar la sesión actual
current_session: ContextVar[Any] = ContextVar("current_session", default=None)

class DBSessionManager: # cambiar a DBContextManager
    def __enter__(self) -> Any:
        """
        Inicia la sesión cuando entra en el contexto 'with'.
        """
        
        if session := db_connection.get_new_session():
            session.begin()
            # Establece la sesión en el contexto actual
            token = current_session.set(session)
            self._token = token

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Realiza el rollback o commit y cierra la sesión cuando sale del contexto 'with'.
        """
        
        if session := current_session.get():
            if exc_type:
                session.rollback()
            else:
                session.commit()
            session.close()
            # Restaura el estado anterior del contexto
            current_session.reset(self._token)

class DBTestSessionManager(DBSessionManager):
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Realiza el rollback y cierra la sesión cuando sale del contexto 'with'.
        """
        if session := current_session.get():
            session.rollback()
            session.close()
            # Restaura el estado anterior del contexto
            current_session.reset(self._token)
