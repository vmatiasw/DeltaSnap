from sqlalchemy import Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.orderinglist import ordering_list
import random


class Base(DeclarativeBase): ...


SET_DE_CARTAS = ["c1", "c2", "c3"]

# JUGADOR ------------------------------------------------------


class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_creator: Mapped[Boolean] = mapped_column(Boolean, default=False)
    game_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("games.id"), nullable=False
    )
    game: Mapped["Game"] = relationship("Game", back_populates="players")
    order: Mapped[int] = mapped_column(Integer, nullable=True)
    card_deck: Mapped[list["Card"]] = relationship(
        "Card", back_populates="player", cascade="all, delete-orphan"
    )


# PARTIDA ------------------------------------------------------


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    game_name: Mapped[str] = mapped_column(String(255), nullable=False)
    creator_name: Mapped[str] = mapped_column(String(255), nullable=False)
    started: Mapped[Boolean] = mapped_column(Boolean, default=False)
    players: Mapped[list[Player]] = relationship(
        "Player",
        back_populates="game",
        cascade="all",
        order_by="Player.order",
        collection_class=ordering_list("order"),
    )
    turn_start_time: Mapped[str] = mapped_column(
        String(255), nullable=False, default="0"
    )
    turn_duration: Mapped[int] = mapped_column(Integer, nullable=False, default=0)


# CARTA -------------------------------------------------------


class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    card: Mapped[str] = mapped_column(
        String(255), nullable=False, default=lambda: random.choice(SET_DE_CARTAS)
    )
    revealed: Mapped[Boolean] = mapped_column(Boolean, default=True)
    player: Mapped["Player"] = relationship("Player", back_populates="card_deck")
    player_id = mapped_column(Integer, ForeignKey("players.id"))
