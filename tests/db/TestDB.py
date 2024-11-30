from tests.db.DBConnection.db_connection_manajer import db_connection
from tests.db.DBTransaction.db_transaction_manajer import DBTransaction
from tests.db.GameFactory import GameFactory

class TestDB:
    def __init__(self) -> None:
        self.session = DBTransaction(db_connection.get_new_session())
        self.game = GameFactory(self.session)
    
    def setup_data(self):
        '''
        Función para crear una base de datos de prueba representativa de una real.
        '''
        partida = self.game.crear_partida()
        self.game.unir_jugadores(partida, numero_de_jugadores=2)
        
        partida2 = self.game.crear_partida()
        self.game.unir_jugadores(partida2, numero_de_jugadores=2)
        
        self.session.commit()
