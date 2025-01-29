import copy
import pytest

from src.deltadb import DBCapturer, Changes, Created, Deleted
from tests.db.game_test.GameFactory import GameFactory
from tests.db.repository.IRepository import IRepository

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
            ("cartas", 1),
            ("cartas", 2),
            ("cartas", 3),
            ("cartas", 4),
            ("cartas", 5),
            ("cartas", 6),
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
            ("jugadores", 1): {
                "nombre": ("Creador", "#field don't exist"),
                "es_creador": ("#field don't exist", True),
                "mazo_cartas": (set(), {("cartas", 1), ("cartas", 2)}),
            },
            ("jugadores", 2): {"mazo_cartas": (set(), {("cartas", 4), ("cartas", 3)})},
            ("jugadores", 3): {"mazo_cartas": (set(), {("cartas", 5), ("cartas", 6)})},
            ("partidas", 1): {
                "inicio_turno": ("0", "2021-10-10T10:00:00Z"),
                "iniciada": (False, True),
                "duracion_turno": (0, 60),
            },
        }

    # Methods tests
    def test_remove_tables_empty_case(self, differences):
        """
        Test the remove_tables method when no tables are removed.
        """
        changes, created, deleted = copy.deepcopy(differences)
        assert created.remove_tables([]) == {
            ("cartas", 1),
            ("cartas", 2),
            ("cartas", 3),
            ("cartas", 4),
            ("cartas", 5),
            ("cartas", 6),
        }
        assert deleted.remove_tables([]) == set()
        assert changes.remove_tables([]) == {
            ("partidas", 1): {
                "duracion_turno": (0, 60),
                "inicio_turno": ("0", "2021-10-10T10:00:00Z"),
                "iniciada": (False, True),
            },
            ("jugadores", 1): {
                "nombre": ("Creador", "#field don't exist"),
                "es_creador": ("#field don't exist", True),
                "mazo_cartas": (set(), {("cartas", 1), ("cartas", 2)}),
            },
            ("jugadores", 2): {"mazo_cartas": (set(), {("cartas", 3), ("cartas", 4)})},
            ("jugadores", 3): {"mazo_cartas": (set(), {("cartas", 6), ("cartas", 5)})},
        }

    def test_ignore_fields_changes_multiple(self, differences):
        """
        Test the ignore_fields_changes method with multiple fields to ignore.
        """
        changes, _, _ = copy.deepcopy(differences)

        assert changes.ignore_fields_changes(
            {"partidas": {"iniciada", "duracion_turno"}, "jugadores": {"nombre"}}
        ) == {
            ("partidas", 1): {
                "duracion_turno": ("#change ignored", "#change ignored"),
                "inicio_turno": ("0", "2021-10-10T10:00:00Z"),
                "iniciada": ("#change ignored", "#change ignored"),
            },
            ("jugadores", 1): {
                "nombre": ("#change ignored", "#change ignored"),
                "es_creador": ("#field don't exist", True),
                "mazo_cartas": (set(), {("cartas", 1), ("cartas", 2)}),
            },
            ("jugadores", 2): {"mazo_cartas": (set(), {("cartas", 3), ("cartas", 4)})},
            ("jugadores", 3): {"mazo_cartas": (set(), {("cartas", 6), ("cartas", 5)})},
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
        assert created.get_schema() == {"cartas"}
        assert not deleted.get_schema()
        assert changes.get_schema() == {
            "partidas": {"iniciada", "duracion_turno", "inicio_turno"},
            "jugadores": {"nombre", "es_creador", "mazo_cartas"},
        }

    def test_get_inverted_capture(self, differences):
        """
        Test the get_inverted_capture method.
        """
        changes, created, deleted = differences
        assert created.get_inverted_capture() == {"cartas": {1, 2, 3, 4, 5, 6}}
        assert not deleted.get_inverted_capture()
        assert changes.get_inverted_capture() == {
            "partidas": {"duracion_turno": {1}, "inicio_turno": {1}, "iniciada": {1}},
            "jugadores": {"nombre": {1}, "es_creador": {1}, "mazo_cartas": {1, 2, 3}},
        }

    def test_get_frequency(self, differences):
        """
        Test the get_frequency method.
        """
        changes, created, deleted = differences
        assert created.get_frequency() == {"cartas": 6}
        assert not deleted.get_frequency()
        assert changes.get_frequency() == {
            "partidas": {
                "#table frequency": 1,
                "duracion_turno": 1,
                "inicio_turno": 1,
                "iniciada": 1,
            },
            "jugadores": {
                "#table frequency": 3,
                "nombre": 1,
                "es_creador": 1,
                "mazo_cartas": 3,
            },
        }

    def test_remove_tables(self, differences):
        """
        Test the remove_tables method with a copy of the instances.
        """
        changes, created, deleted = copy.deepcopy(differences)

        assert created.remove_tables(["jugadores"]) == {
            ("cartas", 3),
            ("cartas", 6),
            ("cartas", 5),
            ("cartas", 2),
            ("cartas", 1),
            ("cartas", 4),
        }

        assert not deleted.remove_tables(["jugadores"])
        assert changes.remove_tables(["jugadores"]) == {
            ("partidas", 1): {
                "inicio_turno": ("0", "2021-10-10T10:00:00Z"),
                "iniciada": (False, True),
                "duracion_turno": (0, 60),
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
            ("cartas", 5),
            ("cartas", 1),
            ("cartas", 4),
            ("cartas", 3),
            ("cartas", 6),
            ("cartas", 2),
        }
        assert deleted == set()
        assert changes == {
            ("jugadores", 1): {
                "nombre": ("Creador", "#field don't exist"),
                "es_creador": ("#field don't exist", True),
                "mazo_cartas": (set(), {("cartas", 1), ("cartas", 2)}),
            },
            ("jugadores", 2): {"mazo_cartas": (set(), {("cartas", 3), ("cartas", 4)})},
            ("jugadores", 3): {"mazo_cartas": (set(), {("cartas", 6), ("cartas", 5)})},
            ("partidas", 1): {
                "inicio_turno": ("0", "2021-10-10T10:00:00Z"),
                "iniciada": (False, True),
                "duracion_turno": (0, 60),
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
        assert changes[("jugadores", 1)] == {
            "nombre": ("Creador", "#field don't exist"),
            "es_creador": ("#field don't exist", True),
            "mazo_cartas": (set(), {("cartas", 1), ("cartas", 2)}),
        }

    def test_setitem(self, differences):
        """
        Test the setitem method.
        """
        changes, _, _ = copy.deepcopy(differences)
        changes[("juego", 1)] = {
            "nombre": ("Tenis", "Basket"),
        }

        assert changes[("juego", 1)] == {
            "nombre": ("Tenis", "Basket"),
        }

    def test_contains(self, differences):
        """
        Test the contains method.
        """
        changes, created, deleted = differences
        assert ("cartas", 1) in created
        assert ("papa", 10) not in deleted
        assert ("partidas", 1) in changes
        assert ("jugadores", 1) in changes

    def test_delitem(self, differences):
        """
        Test the delitem method.
        """
        changes, created, deleted = copy.deepcopy(differences)
        del changes[("jugadores", 1)]
        assert ("jugadores", 1) not in changes
        assert changes == {
            ("jugadores", 2): {"mazo_cartas": (set(), {("cartas", 3), ("cartas", 4)})},
            ("jugadores", 3): {"mazo_cartas": (set(), {("cartas", 6), ("cartas", 5)})},
            ("partidas", 1): {
                "inicio_turno": ("0", "2021-10-10T10:00:00Z"),
                "iniciada": (False, True),
                "duracion_turno": (0, 60),
            },
        }

    def test_changes_dict(self, differences):
        changes, _, _ = differences
        assert changes.keys() == {
            ("jugadores", 1),
            ("jugadores", 2),
            ("jugadores", 3),
            ("partidas", 1),
        }
        assert dict(changes.items()) == {
            ("jugadores", 1): {
                "nombre": ("Creador", "#field don't exist"),
                "es_creador": ("#field don't exist", True),
                "mazo_cartas": (set(), {("cartas", 1), ("cartas", 2)}),
            },
            ("jugadores", 2): {"mazo_cartas": (set(), {("cartas", 3), ("cartas", 4)})},
            ("jugadores", 3): {"mazo_cartas": (set(), {("cartas", 6), ("cartas", 5)})},
            ("partidas", 1): {
                "inicio_turno": ("0", "2021-10-10T10:00:00Z"),
                "iniciada": (False, True),
                "duracion_turno": (0, 60),
            },
        }

    def test_data_sets(self, differences):
        _, created, deleted = copy.deepcopy(differences)

        created |= {("dino", 7)}
        assert created == {
            ("cartas", 1),
            ("cartas", 2),
            ("cartas", 3),
            ("cartas", 4),
            ("cartas", 5),
            ("cartas", 6),
            ("dino", 7),
        }
        assert created.intersection({("cartas", 1), ("cartas", 2)}) == {
            ("cartas", 1),
            ("cartas", 2),
        }
        assert created - {("cartas", 1), ("cartas", 2)} == {
            ("cartas", 3),
            ("cartas", 4),
            ("cartas", 5),
            ("cartas", 6),
            ("dino", 7),
        }
        assert deleted & {("cartas", 1), ("cartas", 2)} == set()
