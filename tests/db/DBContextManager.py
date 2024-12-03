from typing import Any
from contextvars import ContextVar

# ContextVar para almacenar la sesión actual
current_session: ContextVar[Any] = ContextVar("current_session", default=None)

class DBContextManager():
    def __init__(self, session = None) -> None:
        self._session = session
    
    def __enter__(self) -> Any:
        """
        Inicia la sesión cuando entra en el contexto 'with'.
        """
        
        if self._session:
            self._session.begin()
        
        token = current_session.set(self._session)
        self._token = token

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Realiza el rollback o commit y cierra la sesión cuando sale del contexto 'with'.
        """
        
        if self._session:
            if exc_type:
                self._session.rollback()
            else:
                self._session.commit()
            self._session.close()
        
        current_session.reset(self._token)

class DBTestContextManager(DBContextManager):
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Realiza el rollback y cierra la sesión cuando sale del contexto 'with'.
        """
        if self._session:
            self._session.rollback()
            self._session.close()
        
        current_session.reset(self._token)
