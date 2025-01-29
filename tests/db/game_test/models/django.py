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


class Player(Base):
    name: models.CharField = models.CharField(max_length=255, null=False)
    is_creator: models.BooleanField = models.BooleanField(default=False)
    game_id: models.ForeignKey = models.ForeignKey(
        "Game", on_delete=models.CASCADE, related_name="players"
    )
    order: models.IntegerField = models.IntegerField(null=True)

    class Meta:
        db_table = "players"
        app_label = APP_LABEL

    def __str__(self):
        return self.name


# PARTIDA ------------------------------------------------------


class Game(Base):
    game_name: models.CharField = models.CharField(max_length=255, null=False)
    creator_name: models.CharField = models.CharField(max_length=255, null=False)
    started: models.BooleanField = models.BooleanField(default=False)
    turn_start_time: models.CharField = models.CharField(max_length=255, default="0")
    turn_duration: models.IntegerField = models.IntegerField(default=0)

    class Meta:
        db_table = "games"
        app_label = APP_LABEL

    def __str__(self):
        return self.game_name


# CARTA ------------------------------------------------------


class Card(Base):
    card: models.CharField = models.CharField(
        max_length=255, default=lambda: random.choice(SET_DE_CARTAS)
    )
    revealed: models.BooleanField = models.BooleanField(default=True)
    player_id: models.ForeignKey = models.ForeignKey(
        Player, on_delete=models.SET_NULL, null=True, related_name="card_deck"
    )

    class Meta:
        db_table = "cards"
        app_label = APP_LABEL

    def __str__(self):
        return self.card
