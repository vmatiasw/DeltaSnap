from typing import Any

MOCK_GMT_TIME_ZT = "2021-10-10T10:00:00Z"
TIMER_SECONDS_PER_TURN = 60
TOTAL_FACE_CARD_COUNT = 6


class GameFactory:

    def __init__(self, repository: Any):
        self.repository = repository

    def create_game(self) -> Any:
        """Creates an initial game with a creator and adds it to the database."""
        game = self.repository.instance_model(
            "Game",
            game_name="Game",
            creator_name="Creator",
            started=False,
        )
        game_id = self.repository.get_key(game)
        creator = self.repository.instance_model(
            "Player", name="Creator", game_id=game_id, is_creator=True, order=0
        )
        self.repository.append(game.players, creator)

        self.repository.add(creator)
        self.repository.add(game)
        self.repository.flush()
        return game

    def add_players(self, game: Any, player_count: int = 1) -> list[Any]:
        """Adds players to an existing game."""
        assert not game.started, "The game has already started"

        assert player_count < 4, "You cannot add more than 4 players to the game"

        if player_count == 0:
            return []

        new_players = []
        for i in range(player_count):
            game_id = self.repository.get_key(game)
            new_player = self.repository.instance_model(
                "Player",
                name=f"Player{i+2}",
                game_id=game_id,
                is_creator=False,
                order=self.repository.count(game.players),
            )

            self.repository.add(new_player)
            self.repository.append(game.players, new_player)
            new_players.append(new_player)
            self.repository.flush()

        self.repository.flush()
        return new_players

    def start_game(self, game: Any) -> Any:
        """Starts the game, deals cards, and updates the game state."""
        assert not game.started, "The game has already started"

        game.started = True
        game.turn_start_time = MOCK_GMT_TIME_ZT
        game.turn_duration = TIMER_SECONDS_PER_TURN

        self.__deal_cards(game, 3, 2)

        self.repository.flush([game])
        return game

    def __deal_cards(self, game: Any, revealed_card_count: int, cards_per_player: int):
        """Deals the cards among the players of a game."""
        assert game.started, "The game has not been started"

        players = self.repository.get_list(game.players)
        # Create face cards
        for player in players:
            for i in range(cards_per_player - self.repository.count(player.card_deck)):
                player_id = self.repository.get_key(player)
                card = self.repository.instance_model(
                    "Card", player_id=player_id, revealed=(i < revealed_card_count)
                )

                self.repository.add(card)
                self.repository.append(player.card_deck, card)

        self.repository.flush()
