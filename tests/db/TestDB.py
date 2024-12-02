from tests.db.GameFactory import GameFactory

class TestDB:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.game = GameFactory(repository)
    
    def setup_data(self):
        '''
        Función para crear una base de datos de prueba representativa de una real.
        '''
        partida = self.game.crear_partida()
        self.game.unir_jugadores(partida, numero_de_jugadores=2)
        
        partida2 = self.game.crear_partida()
        self.game.unir_jugadores(partida2, numero_de_jugadores=2)
        
        self.repository.commit()
