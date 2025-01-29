from tests.db.game_test.GameFactory import GameFactory
from tests.db.repository.IRepository import IRepository


def setup_db_data(repository: IRepository, game: GameFactory):
    """
    Prepares the database with some data for testing purposes.
    """
    game.add_players(game.create_game(), player_count=2)
    game.add_players(game.create_game(), player_count=2)

    repository.commit()  # FIXME: is it okay to commit here?
