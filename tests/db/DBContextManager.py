from typing import Any

from tests.db.DBConnection.db_connection_manajer import db_connection

class DBContextManager:
    def __init__(self):
        self.session = None
    
    def __enter__(self) -> Any:
        """
        Inicia la sesión cuando entra en el contexto 'with'.
        """
        self.session = db_connection.get_new_session()
        self.session.begin()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Realiza el rollback o commit y cierra la sesión cuando sale del contexto 'with'.
        """
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()
        
class DBTestContextManager(DBContextManager):

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Realiza el rollback y cierra la sesión cuando sale del contexto 'with'.
        """
        self.session.rollback()
        self.session.close()