from tests.db.game_test.GameFactory import GameFactory
from tests.db.repository.IRepository import IRepository


def setup_db_data(repository: IRepository, game: GameFactory):
    """
    Prepares the database with some data for testing purposes.
    """
    partida = game.crear_partida()
    game.unir_jugadores(partida, numero_de_jugadores=2)

    partida2 = game.crear_partida()
    game.unir_jugadores(partida2, numero_de_jugadores=2)

    repository.commit()
