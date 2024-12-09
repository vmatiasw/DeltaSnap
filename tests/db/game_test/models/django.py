from django.db import models
import random
from tests.db.config import APP_LABEL

SET_DE_CARTAS = ["c1", "c2", "c3"]


class Base(models.Model):
    class Meta:
        abstract = True
        app_label = APP_LABEL

    id: models.AutoField = models.AutoField(primary_key=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"


# JUGADOR ------------------------------------------------------


class Jugador(Base):
    nombre: models.CharField = models.CharField(max_length=255, null=False)
    es_creador: models.BooleanField = models.BooleanField(default=False)
    partida_id: models.ForeignKey = models.ForeignKey(
        "Partida", on_delete=models.CASCADE, related_name="jugadores"
    )
    orden: models.IntegerField = models.IntegerField(null=True)

    class Meta:
        db_table = "jugadores"
        app_label = APP_LABEL

    def __str__(self):
        return self.nombre


# PARTIDA ------------------------------------------------------


class Partida(Base):
    nombre_partida: models.CharField = models.CharField(max_length=255, null=False)
    nombre_creador: models.CharField = models.CharField(max_length=255, null=False)
    iniciada: models.BooleanField = models.BooleanField(default=False)
    inicio_turno: models.CharField = models.CharField(max_length=255, default="0")
    duracion_turno: models.IntegerField = models.IntegerField(default=0)

    class Meta:
        db_table = "partidas"
        app_label = APP_LABEL

    def __str__(self):
        return self.nombre_partida


# CARTA ------------------------------------------------------


class Carta(Base):
    carta: models.CharField = models.CharField(
        max_length=255, default=lambda: random.choice(SET_DE_CARTAS)
    )
    revelada: models.BooleanField = models.BooleanField(default=True)
    jugador_id: models.ForeignKey = models.ForeignKey(
        Jugador, on_delete=models.SET_NULL, null=True, related_name="mazo_cartas"
    )

    class Meta:
        db_table = "cartas"
        app_label = APP_LABEL

    def __str__(self):
        return self.carta
