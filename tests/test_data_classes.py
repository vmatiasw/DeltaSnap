import copy

from src.deltasnap import Changes, Created, Deleted

# TODO: dividir clase en 3 o 4 y divicir tests por change, deleted y created


class TestDataClasses:
    """
    Class to test the data classes instances (Changes, Creation, Deletion).
    """

    # Initialization tests
    def test_created_class_initialization(self, differences):
        """
        Test the initialization of the Created class.
        """
        changes, created, deleted = differences
        assert isinstance(created, Created)
        assert isinstance(created, set)
        assert created == {
            ("cards", 1),
            ("cards", 2),
            ("cards", 3),
            ("cards", 4),
            ("cards", 5),
            ("cards", 6),
        }

    def test_deleted_class_initialization(self, differences):
        """
        Test the initialization of the Deleted class.
        """
        _, _, deleted = differences
        assert isinstance(deleted, Deleted)
        assert isinstance(deleted, set)
        assert deleted == set()

    def test_changes_class_initialization(self, differences):
        """
        Test the initialization of the Changes class.
        """
        changes, _, _ = differences
        assert isinstance(changes, Changes)
        assert isinstance(changes, dict)
        assert changes == {
            ("players", 1): {
                "name": ("Creator", "#field don't exist"),
                "is_creator": ("#field don't exist", True),
                "card_deck": (set(), {("cards", 1), ("cards", 2)}),
            },
            ("players", 2): {"card_deck": (set(), {("cards", 4), ("cards", 3)})},
            ("players", 3): {"card_deck": (set(), {("cards", 5), ("cards", 6)})},
            ("games", 1): {
                "turn_start_time": ("0", "2021-10-10T10:00:00Z"),
                "started": (False, True),
                "turn_duration": (0, 60),
            },
        }

    # Methods tests
    def test_remove_tables_empty_case(self, differences):
        """
        Test the remove_tables method when no tables are removed.
        """
        changes, created, deleted = copy.deepcopy(differences)
        assert created.remove_tables([]) == {
            ("cards", 1),
            ("cards", 2),
            ("cards", 3),
            ("cards", 4),
            ("cards", 5),
            ("cards", 6),
        }
        assert deleted.remove_tables([]) == set()
        assert changes.remove_tables([]) == {
            ("games", 1): {
                "turn_duration": (0, 60),
                "turn_start_time": ("0", "2021-10-10T10:00:00Z"),
                "started": (False, True),
            },
            ("players", 1): {
                "name": ("Creator", "#field don't exist"),
                "is_creator": ("#field don't exist", True),
                "card_deck": (set(), {("cards", 1), ("cards", 2)}),
            },
            ("players", 2): {"card_deck": (set(), {("cards", 3), ("cards", 4)})},
            ("players", 3): {"card_deck": (set(), {("cards", 6), ("cards", 5)})},
        }

    def test_ignore_fields_changes_multiple(self, differences):
        """
        Test the ignore_fields_changes method with multiple fields to ignore.
        """
        changes, _, _ = copy.deepcopy(differences)

        assert changes.ignore_fields_changes(
            {"games": {"started", "turn_duration"}, "players": {"name"}}
        ) == {
            ("games", 1): {
                "turn_duration": ("#change ignored", "#change ignored"),
                "turn_start_time": ("0", "2021-10-10T10:00:00Z"),
                "started": ("#change ignored", "#change ignored"),
            },
            ("players", 1): {
                "name": ("#change ignored", "#change ignored"),
                "is_creator": ("#field don't exist", True),
                "card_deck": (set(), {("cards", 1), ("cards", 2)}),
            },
            ("players", 2): {"card_deck": (set(), {("cards", 3), ("cards", 4)})},
            ("players", 3): {"card_deck": (set(), {("cards", 6), ("cards", 5)})},
        }

    def test_get_schema_empty_case(self):
        """
        Test the get_schema method when there are no changes.
        """
        empty_changes = Changes({})
        assert empty_changes.get_schema() == {}
        assert not empty_changes.get_inverted_capture()
        assert empty_changes.get_frequency() == {}

        empty_deleted = Deleted(set())
        assert empty_deleted.get_schema() == set()
        assert not empty_deleted.get_inverted_capture()
        assert empty_deleted.get_frequency() == {}

        empty_created = Created(set())
        assert empty_created.get_schema() == set()
        assert not empty_created.get_inverted_capture()
        assert empty_created.get_frequency() == {}

    def test_get_schema(self, differences):
        """
        Test the get_schema method.
        """
        changes, created, deleted = differences
        assert created.get_schema() == {"cards"}
        assert not deleted.get_schema()
        assert changes.get_schema() == {
            "games": {"started", "turn_duration", "turn_start_time"},
            "players": {"name", "is_creator", "card_deck"},
        }

    def test_get_inverted_capture(self, differences):
        """
        Test the get_inverted_capture method.
        """
        changes, created, deleted = differences
        assert created.get_inverted_capture() == {"cards": {1, 2, 3, 4, 5, 6}}
        assert not deleted.get_inverted_capture()
        assert changes.get_inverted_capture() == {
            "games": {"turn_duration": {1}, "turn_start_time": {1}, "started": {1}},
            "players": {"name": {1}, "is_creator": {1}, "card_deck": {1, 2, 3}},
        }

    def test_get_frequency(self, differences):
        """
        Test the get_frequency method.
        """
        changes, created, deleted = differences
        assert created.get_frequency() == {"cards": 6}
        assert not deleted.get_frequency()
        assert changes.get_frequency() == {
            "games": {
                "#table frequency": 1,
                "turn_duration": 1,
                "turn_start_time": 1,
                "started": 1,
            },
            "players": {
                "#table frequency": 3,
                "name": 1,
                "is_creator": 1,
                "card_deck": 3,
            },
        }

    def test_remove_tables(self, differences):
        """
        Test the remove_tables method with a copy of the instances.
        """
        changes, created, deleted = copy.deepcopy(differences)

        assert created.remove_tables(["players"]) == {
            ("cards", 3),
            ("cards", 6),
            ("cards", 5),
            ("cards", 2),
            ("cards", 1),
            ("cards", 4),
        }

        assert not deleted.remove_tables(["players"])
        assert changes.remove_tables(["players"]) == {
            ("games", 1): {
                "turn_start_time": ("0", "2021-10-10T10:00:00Z"),
                "started": (False, True),
                "turn_duration": (0, 60),
            }
        }

        assert isinstance(created, Created)
        assert isinstance(deleted, Deleted)
        assert isinstance(changes, Changes)

    # Magic methods tests
    def test_eq(self, differences):
        """
        Test the eq method.
        """
        changes, created, deleted = differences
        assert created == {
            ("cards", 5),
            ("cards", 1),
            ("cards", 4),
            ("cards", 3),
            ("cards", 6),
            ("cards", 2),
        }
        assert deleted == set()
        assert changes == {
            ("players", 1): {
                "name": ("Creator", "#field don't exist"),
                "is_creator": ("#field don't exist", True),
                "card_deck": (set(), {("cards", 1), ("cards", 2)}),
            },
            ("players", 2): {"card_deck": (set(), {("cards", 3), ("cards", 4)})},
            ("players", 3): {"card_deck": (set(), {("cards", 6), ("cards", 5)})},
            ("games", 1): {
                "turn_start_time": ("0", "2021-10-10T10:00:00Z"),
                "started": (False, True),
                "turn_duration": (0, 60),
            },
        }

    def test_bool(self, differences):
        """
        Test the bool method.
        """
        changes, created, deleted = differences
        assert bool(created)
        assert not bool(deleted)
        assert bool(changes)

    def test_len(self, differences):
        """
        Test the len method.
        """
        changes, created, deleted = differences
        assert len(created) == 6
        assert len(deleted) == 0
        assert len(changes) == 4

    def test_iter(self, differences):
        """
        Test the iter method.
        """
        changes, created, deleted = differences
        for record in created:
            assert record

        for record in deleted:
            assert record

        for record in changes:
            assert record

    def test_getitem(self, differences):
        """
        Test the getitem method.
        """
        changes, _, _ = differences
        assert changes[("players", 1)] == {
            "name": ("Creator", "#field don't exist"),
            "is_creator": ("#field don't exist", True),
            "card_deck": (set(), {("cards", 1), ("cards", 2)}),
        }

    def test_setitem(self, differences):
        """
        Test the setitem method.
        """
        changes, _, _ = copy.deepcopy(differences)
        changes[("juego", 1)] = {
            "name": ("Tenis", "Basket"),
        }

        assert changes[("juego", 1)] == {
            "name": ("Tenis", "Basket"),
        }

    def test_contains(self, differences):
        """
        Test the contains method.
        """
        changes, created, deleted = differences
        assert ("cards", 1) in created
        assert ("papa", 10) not in deleted
        assert ("games", 1) in changes
        assert ("players", 1) in changes

    def test_delitem(self, differences):
        """
        Test the delitem method.
        """
        changes, created, deleted = copy.deepcopy(differences)
        del changes[("players", 1)]
        assert ("players", 1) not in changes
        assert changes == {
            ("players", 2): {"card_deck": (set(), {("cards", 3), ("cards", 4)})},
            ("players", 3): {"card_deck": (set(), {("cards", 6), ("cards", 5)})},
            ("games", 1): {
                "turn_start_time": ("0", "2021-10-10T10:00:00Z"),
                "started": (False, True),
                "turn_duration": (0, 60),
            },
        }

    def test_changes_dict(self, differences):
        changes, _, _ = differences
        assert changes.keys() == {
            ("players", 1),
            ("players", 2),
            ("players", 3),
            ("games", 1),
        }
        assert dict(changes.items()) == {
            ("players", 1): {
                "name": ("Creator", "#field don't exist"),
                "is_creator": ("#field don't exist", True),
                "card_deck": (set(), {("cards", 1), ("cards", 2)}),
            },
            ("players", 2): {"card_deck": (set(), {("cards", 3), ("cards", 4)})},
            ("players", 3): {"card_deck": (set(), {("cards", 6), ("cards", 5)})},
            ("games", 1): {
                "turn_start_time": ("0", "2021-10-10T10:00:00Z"),
                "started": (False, True),
                "turn_duration": (0, 60),
            },
        }

    def test_data_sets(self, differences):
        _, created, deleted = copy.deepcopy(differences)

        created |= {("dino", 7)}
        assert created == {
            ("cards", 1),
            ("cards", 2),
            ("cards", 3),
            ("cards", 4),
            ("cards", 5),
            ("cards", 6),
            ("dino", 7),
        }
        assert created.intersection({("cards", 1), ("cards", 2)}) == {
            ("cards", 1),
            ("cards", 2),
        }
        assert created - {("cards", 1), ("cards", 2)} == {
            ("cards", 3),
            ("cards", 4),
            ("cards", 5),
            ("cards", 6),
            ("dino", 7),
        }
        assert deleted & {("cards", 1), ("cards", 2)} == set()
