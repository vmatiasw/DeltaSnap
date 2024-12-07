from sqlalchemy import Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.orderinglist import ordering_list
import random


class Base(DeclarativeBase): ...


SET_DE_CARTAS = ["c1", "c2", "c3"]

# JUGADOR ------------------------------------------------------


class Jugador(Base):
    __tablename__ = "jugadores"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    es_creador: Mapped[Boolean] = mapped_column(Boolean, default=False)
    partida_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("partidas.id"), nullable=False
    )
    partida = relationship("Partida", back_populates="jugadores")
    orden: Mapped[int] = mapped_column(Integer, nullable=True)
    mazo_cartas: Mapped[list["Carta"]] = relationship(
        "Carta", back_populates="jugador", cascade="all, delete-orphan"
    )


# PARTIDA ------------------------------------------------------


class Partida(Base):
    # PARTIDA -----------------------
    __tablename__ = "partidas"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    nombre_partida = mapped_column(String(255), nullable=False)
    nombre_creador = mapped_column(String(255), nullable=False)
    iniciada = mapped_column(Boolean, default=False)
    jugadores: Mapped[list[Jugador]] = relationship(
        "Jugador",
        back_populates="partida",
        cascade="all",
        order_by="Jugador.orden",
        collection_class=ordering_list("orden"),
    )

    # JUEGO -----------------------
    inicio_turno = mapped_column(String(255), nullable=False, default="0")
    duracion_turno = mapped_column(Integer, nullable=False, default=0)


# Carta --------------------------------------------------


class Carta(Base):

    __tablename__ = "cartas"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True
    )
    carta: Mapped[str] = mapped_column(
        String(255), nullable=False, default=lambda: random.choice(SET_DE_CARTAS)
    )
    revelada: Mapped[Boolean] = mapped_column(Boolean, default=True)
    jugador = relationship("Jugador", back_populates="mazo_cartas")
    jugador_id = mapped_column(Integer, ForeignKey("jugadores.id"))
