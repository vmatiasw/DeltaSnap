import pytest

from DeltaDB import DBCapturer
from tests.db.repository.IRepository import IRepository


@pytest.mark.usefixtures("db_capturer", "game")
class TestCapture:
    """
    Class to test the data capture.
    """

    def test_equal_captures(self, repository: IRepository, db_capturer: DBCapturer):
        """
        Test the equality of the captures.
        """
        partida1 = repository.get("Partida", 1)
        partida2 = repository.get("Partida", 2)
        jugador1 = repository.get("Jugador", 1)
        jugador2 = repository.get("Jugador", 2)
        jugador3 = repository.get("Jugador", 3)
        jugador4 = repository.get("Jugador", 4)
        jugador5 = repository.get("Jugador", 5)
        jugador6 = repository.get("Jugador", 6)

        capture1 = db_capturer.capture_all_records()
        capture2 = db_capturer.capture_related_records([partida1, partida2])
        capture3 = db_capturer.capture_records(
            [
                partida1,
                partida2,
                jugador1,
                jugador2,
                jugador3,
                jugador4,
                jugador5,
                jugador6,
            ]
        )

        assert capture1 == capture2 == capture3

    def test_capture_records(self, db_capturer: DBCapturer, repository: IRepository):
        """
        Test the capture of records.
        """
        partida1 = repository.get("Partida", 1)
        partida2 = repository.get("Partida", 2)

        assert db_capturer.capture_records([partida1, partida2]) == {
            ("partidas", 1): {
                "id": 1,
                "nombre_partida": "Partida",
                "nombre_creador": "Creador",
                "iniciada": False,
                "inicio_turno": "0",
                "duracion_turno": 0,
            },
            ("partidas", 2): {
                "id": 2,
                "nombre_partida": "Partida",
                "nombre_creador": "Creador",
                "iniciada": False,
                "inicio_turno": "0",
                "duracion_turno": 0,
            },
        }

    def test_capture_related_records(
        self, db_capturer: DBCapturer, repository: IRepository
    ):
        """
        Test the capture of related records.
        """
        partida = repository.get("Partida", 1)

        assert db_capturer.capture_related_records([partida]) == {
            ("partidas", 1): {
                "id": 1,
                "nombre_partida": "Partida",
                "nombre_creador": "Creador",
                "iniciada": False,
                "inicio_turno": "0",
                "duracion_turno": 0,
            },
            ("jugadores", 3): {
                "id": 3,
                "nombre": "Jugador3",
                "es_creador": False,
                "partida_id": ("partidas", 1),
                "orden": 2,
            },
            ("jugadores", 2): {
                "id": 2,
                "nombre": "Jugador2",
                "es_creador": False,
                "partida_id": ("partidas", 1),
                "orden": 1,
            },
            ("jugadores", 1): {
                "id": 1,
                "nombre": "Creador",
                "es_creador": True,
                "partida_id": ("partidas", 1),
                "orden": 0,
            },
        }

    def test_capture_all_records(self, db_capturer: DBCapturer):
        """
        Test the capture of all records.
        """
        assert db_capturer.capture_all_records() == {
            ("partidas", 1): {
                "id": 1,
                "nombre_partida": "Partida",
                "nombre_creador": "Creador",
                "iniciada": False,
                "inicio_turno": "0",
                "duracion_turno": 0,
            },
            ("partidas", 2): {
                "id": 2,
                "nombre_partida": "Partida",
                "nombre_creador": "Creador",
                "iniciada": False,
                "inicio_turno": "0",
                "duracion_turno": 0,
            },
            ("jugadores", 1): {
                "id": 1,
                "nombre": "Creador",
                "es_creador": True,
                "partida_id": ("partidas", 1),
                "orden": 0,
            },
            ("jugadores", 2): {
                "id": 2,
                "nombre": "Jugador2",
                "es_creador": False,
                "partida_id": ("partidas", 1),
                "orden": 1,
            },
            ("jugadores", 3): {
                "id": 3,
                "nombre": "Jugador3",
                "es_creador": False,
                "partida_id": ("partidas", 1),
                "orden": 2,
            },
            ("jugadores", 4): {
                "id": 4,
                "nombre": "Creador",
                "es_creador": True,
                "partida_id": ("partidas", 2),
                "orden": 0,
            },
            ("jugadores", 5): {
                "id": 5,
                "nombre": "Jugador2",
                "es_creador": False,
                "partida_id": ("partidas", 2),
                "orden": 1,
            },
            ("jugadores", 6): {
                "id": 6,
                "nombre": "Jugador3",
                "es_creador": False,
                "partida_id": ("partidas", 2),
                "orden": 2,
            },
        }
