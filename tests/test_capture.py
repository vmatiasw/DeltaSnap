from src.deltasnap import DBCapturer
from tests.db.repository.IRepository import IRepository


class TestCapture:
    """
    Class to test the data capture.
    """

    def test_equal_captures(self, repository: IRepository, db_capturer: DBCapturer):
        """
        Test the equality of the captures.
        """
        game1 = repository.get("Game", 1)
        game2 = repository.get("Game", 2)
        player1 = repository.get("Player", 1)
        player2 = repository.get("Player", 2)
        player3 = repository.get("Player", 3)
        player4 = repository.get("Player", 4)
        player5 = repository.get("Player", 5)
        player6 = repository.get("Player", 6)

        capture1 = db_capturer.capture_all_records()
        capture2 = db_capturer.capture_related_records([game1, game2])
        capture3 = db_capturer.capture_records(
            [
                game1,
                game2,
                player1,
                player2,
                player3,
                player4,
                player5,
                player6,
            ]
        )

        assert capture1 == capture2
        assert capture2 == capture3

    def test_capture_records(self, db_capturer: DBCapturer, repository: IRepository):
        """
        Test the capture of records.
        """
        game1 = repository.get("Game", 1)
        game2 = repository.get("Game", 2)

        assert db_capturer.capture_records([game1, game2]) == {
            ("games", 1): {
                "id": 1,
                "game_name": "Game",
                "creator_name": "Creator",
                "started": False,
                "turn_start_time": "0",
                "turn_duration": 0,
                "players": {("players", 1), ("players", 2), ("players", 3)},
            },
            ("games", 2): {
                "id": 2,
                "game_name": "Game",
                "creator_name": "Creator",
                "started": False,
                "turn_start_time": "0",
                "turn_duration": 0,
                "players": {("players", 5), ("players", 6), ("players", 4)},
            },
        }

    def test_capture_related_records(
        self, db_capturer: DBCapturer, repository: IRepository
    ):
        """
        Test the capture of related records.
        """
        game = repository.get("Game", 1)

        assert db_capturer.capture_related_records([game]) == {
            ("games", 1): {
                "id": 1,
                "game_name": "Game",
                "creator_name": "Creator",
                "started": False,
                "turn_start_time": "0",
                "turn_duration": 0,
                "players": {("players", 1), ("players", 2), ("players", 3)},
            },
            ("players", 3): {
                "id": 3,
                "name": "Player3",
                "is_creator": False,
                "game_id": ("games", 1),
                "order": 2,
                "card_deck": set(),
            },
            ("players", 2): {
                "id": 2,
                "name": "Player2",
                "is_creator": False,
                "game_id": ("games", 1),
                "order": 1,
                "card_deck": set(),
            },
            ("players", 1): {
                "id": 1,
                "name": "Creator",
                "is_creator": True,
                "game_id": ("games", 1),
                "order": 0,
                "card_deck": set(),
            },
        }

    def test_capture_all_records(self, db_capturer: DBCapturer):
        """
        Test the capture of all records.
        """
        assert db_capturer.capture_all_records() == {
            ("games", 1): {
                "id": 1,
                "game_name": "Game",
                "creator_name": "Creator",
                "started": False,
                "turn_start_time": "0",
                "turn_duration": 0,
                "players": {("players", 1), ("players", 2), ("players", 3)},
            },
            ("games", 2): {
                "id": 2,
                "game_name": "Game",
                "creator_name": "Creator",
                "started": False,
                "turn_start_time": "0",
                "turn_duration": 0,
                "players": {("players", 4), ("players", 5), ("players", 6)},
            },
            ("players", 1): {
                "id": 1,
                "name": "Creator",
                "is_creator": True,
                "game_id": ("games", 1),
                "order": 0,
                "card_deck": set(),
            },
            ("players", 2): {
                "id": 2,
                "name": "Player2",
                "is_creator": False,
                "game_id": ("games", 1),
                "order": 1,
                "card_deck": set(),
            },
            ("players", 3): {
                "id": 3,
                "name": "Player3",
                "is_creator": False,
                "game_id": ("games", 1),
                "order": 2,
                "card_deck": set(),
            },
            ("players", 4): {
                "id": 4,
                "name": "Creator",
                "is_creator": True,
                "game_id": ("games", 2),
                "order": 0,
                "card_deck": set(),
            },
            ("players", 5): {
                "id": 5,
                "name": "Player2",
                "is_creator": False,
                "game_id": ("games", 2),
                "order": 1,
                "card_deck": set(),
            },
            ("players", 6): {
                "id": 6,
                "name": "Player3",
                "is_creator": False,
                "game_id": ("games", 2),
                "order": 2,
                "card_deck": set(),
            },
        }
