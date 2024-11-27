from sqlalchemy import Integer, Boolean, String, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.orderinglist import ordering_list
import random
from random import shuffle
import json

from tests.tools.db.db_setup import Base, engine

SET_DE_CARTAS = ["c1", "c2", "c3"]

# JUGADOR ------------------------------------------------------


class Jugador(Base):
    __tablename__ = 'jugadores'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    es_creador: Mapped[Boolean] = mapped_column(Boolean, default=False)

    id_partida: Mapped[int] = mapped_column(
        Integer, ForeignKey('partidas.id'), nullable=False)
    partidas = relationship("Partida", back_populates="jugadores")

    orden: Mapped[int] = mapped_column(Integer, nullable=True)
    mazo_cartas: Mapped[list['Carta']] = relationship(
        'Carta', back_populates='poseida_por', cascade="all, delete-orphan")
    bloqueado: Mapped[Boolean] = mapped_column(Boolean, default=False)

    @hybrid_property
    def numero_de_cartas(self) -> int:
        return len(self.mazo_cartas)

    @hybrid_property
    def mano_cartas(self) -> list['Carta']:
        return [carta for carta in self.mazo_cartas if carta.revelada]

    def __str__(self):  # pragma: no cover
        return (f"<Jugador(id={self.id}, nombre={self.nombre}, "
                f"es_creador={self.es_creador}, id_partida={self.id_partida}, orden={self.orden}, "
                f"numero_de_cartas={len(self.mazo_cartas)}")
# PARTIDA ------------------------------------------------------


def tablero_random():
    """Genera una lista de 36 fichas de 4 colores distintos mezcladas aleatoriamente
    Returns:
        String: Lista de fichas (Como JSON)
    """
    set_de_fichas = [1 for i in range(9)] + [2 for i in range(9)] + [3 for i in range(9)] + [
        4 for i in range(9)]
    shuffle(set_de_fichas)
    tablero = []
    for i in range(6):
        tablero.append(set_de_fichas[i*6:i*6+6])

    tablero_as_json = json.dumps(tablero)

    return tablero_as_json


class Partida(Base):
    # PARTIDA -----------------------
    __tablename__ = 'partidas'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)
    nombre_partida = mapped_column(String(255), nullable=False)
    nombre_creador = mapped_column(String(255), nullable=False)
    iniciada = mapped_column(Boolean, default=False)
    jugadores: Mapped[list[Jugador]] = relationship(
        'Jugador', back_populates='partidas', cascade="all", order_by='Jugador.orden', collection_class=ordering_list('orden'))

    privada = mapped_column(Boolean, nullable=False, default=False)
    contraseña = mapped_column(String(255), nullable=False, default='')

    @hybrid_property
    def numero_de_jugadores(self) -> int:
        return len(self.jugadores)

    @hybrid_property
    def id_creador(self) -> int | None:
        id_jugador_creador = next(
            (jugador.id for jugador in self.jugadores if jugador.es_creador), None)
        if id_jugador_creador is not None or self.iniciada:
            return id_jugador_creador
        if not self.iniciada:
            raise Exception('No se encontró el jugador creador')
        return None

    # JUEGO -----------------------
    @hybrid_property
    def jugador_del_turno(self) -> Jugador:
        return self.jugadores[0]

    inicio_turno = mapped_column(String(255), nullable=False, default='0')
    duracion_turno = mapped_column(Integer, nullable=False, default=0)
    tablero = mapped_column(String(255), nullable=False, default=tablero_random)
    color_prohibido = mapped_column(Integer, nullable=False, default=0)

    def __str__(self):  # pragma: no cover
        return (f"<Partida(id={self.id}, nombre_partida='{self.nombre_partida}', "
                f"nombre_creador='{self.nombre_creador}', iniciada={self.iniciada}, "
                f"numero_de_jugadores={len(self.jugadores)}, tablero='{self.tablero}')>")

# Carta --------------------------------------------------


class Carta(Base):

    __tablename__ = 'cartas'
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True, autoincrement=True)

    carta: Mapped[str] = mapped_column(
        String(255), nullable=False, default=lambda: random.choice(SET_DE_CARTAS))
    revelada: Mapped[Boolean] = mapped_column(Boolean, default=True)
    bloqueada: Mapped[Boolean] = mapped_column(Boolean, default=False)

    # Las relaciones necesitan que exista además una foreign key
    poseida_por = relationship(
        'Jugador', back_populates='mazo_cartas')
    id_jugador = mapped_column(Integer, ForeignKey('jugadores.id'))

    def __str__(self):  # pragma: no cover
        return (f"<Carta(id={self.id}, carta='{self.carta}', "
                f"revelada={self.revelada}, id_jugador={self.id_jugador})>")
