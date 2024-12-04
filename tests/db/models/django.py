import random
import json
from django.db import models

from tests.db.connection.manajer import db_connection

Model = db_connection.get_base()

SET_DE_CARTAS = ["c1", "c2", "c3"]

# Función para generar el tablero aleatorio


def tablero_random():
    """Genera una lista de 36 fichas de 4 colores distintos mezcladas aleatoriamente
    Returns:
        String: Lista de fichas (como JSON)
    """
    set_de_fichas = (
        [1 for i in range(9)]
        + [2 for i in range(9)]
        + [3 for i in range(9)]
        + [4 for i in range(9)]
    )
    random.shuffle(set_de_fichas)
    tablero = []
    for i in range(6):
        tablero.append(set_de_fichas[i * 6 : i * 6 + 6])
    return json.dumps(tablero)


# Modelo de Jugador
class Jugador(Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    es_creador = models.BooleanField(default=False)
    id_partida = models.ForeignKey(
        "Partida", on_delete=models.CASCADE, related_name="jugadores"
    )
    orden = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre


# Modelo de Partida
class Partida(Model):
    id = models.AutoField(primary_key=True)
    nombre_partida = models.CharField(max_length=255)
    nombre_creador = models.CharField(max_length=255)
    iniciada = models.BooleanField(default=False)
    inicio_turno = models.CharField(max_length=255, default="0")
    duracion_turno = models.IntegerField(default=0)
    tablero = models.TextField(default=tablero_random)

    def __str__(self):
        return self.nombre_partida


# Modelo de Carta
class Carta(Model):
    id = models.AutoField(primary_key=True)
    carta = models.CharField(
        max_length=255, default=lambda: random.choice(SET_DE_CARTAS)
    )
    revelada = models.BooleanField(default=True)
    poseida_por = models.ForeignKey(
        Jugador,
        on_delete=models.CASCADE,
        related_name="mazo_cartas",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.carta
