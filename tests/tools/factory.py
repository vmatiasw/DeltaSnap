from sqlalchemy.orm import Session

from tests.tools.DB.SqlAlchemyDB.models import Partida, Jugador, Carta

MOCK_GMT_TIME_ZT = "2021-10-10T10:00:00Z"
SEGUNDOS_TEMPORIZADOR_TURNO = 60
N_CARTAS_FIGURA_TOTALES = 6

def crear_partida(db: Session, password: str = "") -> Partida:
    '''
    Función para crear una partida.

    Devuelve la partida creada y el jugador creador.

    Valores por defecto:
    - nombre_partida = Partida
    - nombre_creador = Creador
    - iniciada = False
    - tablero = '[[2, 1, 3, 4, 2, 3], [4, 2, 1, 1, 3, 3], [2, 1, 3, 2, 3, 4], [4, 1, 1, 2, 2, 4], [1, 3, 1, 2, 1, 3], [2, 3, 4, 4, 4, 4]]'
    '''
    partida = Partida(nombre_partida="Partida",
                      nombre_creador="Creador",
                      iniciada=False,
                      privada=password != "",
                      contraseña=password,
                      tablero='[[2, 1, 3, 4, 2, 3], [4, 2, 1, 1, 3, 3], [2, 1, 3, 2, 3, 4], [4, 1, 1, 2, 2, 4], [1, 3, 1, 2, 1, 3], [2, 3, 4, 4, 4, 4]]')
    creador = Jugador(nombre="Creador",
                      partidas=partida,
                      es_creador=True,
                      orden=0)
    partida.jugadores.append(creador)

    db.add(creador)
    db.add(partida)

    db.commit()
    return partida

def unir_jugadores(db: Session, partida: Partida, numero_de_jugadores: int = 1) -> list[Jugador]:
    '''
    Función para unir jugadores a una partida.

    Devuelve una lista con los jugadores unidos a la partida.
    Si numero_de_jugadores es 0, devuelve una lista vacía.

    Valores por defecto:
    - partida = Partida
    - numero_de_jugadores = 1
    - nombre = Jugador{i} donde i va desde 2 hasta 4
    '''
    assert partida.iniciada == False, "La partida ya ha sido iniciada"
    assert len(partida.jugadores) <= 4, "La partida ya tiene 4 jugadores"
    assert len(partida.jugadores) > 0, "Y el creador? boludito"
    assert numero_de_jugadores < 4, "No se pueden unir más de 4 jugadores a la partida"

    if numero_de_jugadores == 0:
        return []

    nuevos_jugadores = []
    for i in range(numero_de_jugadores):
        nuevo_jugador = Jugador(nombre=f"Jugador{i+2}", partidas=partida, es_creador=False, orden=len(partida.jugadores))
        db.add(nuevo_jugador)
        partida.jugadores.append(nuevo_jugador)
        nuevos_jugadores.append(nuevo_jugador)
        db.commit()

    db.commit()
    return nuevos_jugadores

def iniciar_partida(db: Session, partida: Partida) -> Partida:
    '''
    Función para iniciar una partida. (y reparte cartas de figura y movimiento)

    Devuelve la partida.

    Valores por defecto:
    - iniciada = True
    - repartir_cartas_figura = 3 cartas por jugador, 3 cartas reveladas
    - repartir_cartas_movimiento = 3 cartas por jugador
    '''
    assert partida.iniciada == False, "La partida ya ha sido iniciada"
    assert len(
        partida.jugadores) > 1, "La partida debe tener al menos 2 jugadores para poder iniciarla"
    assert len(
        partida.jugadores) <= 4, "La partida no puede tener más de 4 jugadores"

    partida.iniciada = True
    partida.inicio_turno = MOCK_GMT_TIME_ZT
    partida.duracion_turno = SEGUNDOS_TEMPORIZADOR_TURNO

    numero_de_cartas_por_jugador = int(
        N_CARTAS_FIGURA_TOTALES/len(partida.jugadores))
    __repartir_cartas(db, partida, 3, numero_de_cartas_por_jugador)

    db.commit()
    return partida


def __repartir_cartas(db: Session, partida: Partida, n_cartas_reveladas, n_cartas_por_jugador):
    '''
    Función para repartir las cartas de figura a los jugadores de una partida.

    Valores por defecto:
    - n_cartas_por_jugador = 3
    '''
    assert n_cartas_por_jugador <= int(
        N_CARTAS_FIGURA_TOTALES/len(partida.jugadores))
    assert partida.iniciada == True, "La partida no ha sido iniciada"
    assert len(
        partida.jugadores) > 1, "La partida debe tener al menos 2 jugadores para poder repartir las cartas de figura"
    assert len(
        partida.jugadores) <= 4, "La partida no puede tener más de 4 jugadores"

    # Crear las cartas de figura
    for jugador in partida.jugadores:
        for i in range(n_cartas_por_jugador - len(jugador.mazo_cartas)):
            carta = Carta(poseida_por=jugador,
                                revelada=(i < n_cartas_reveladas))
            db.add(carta)
            jugador.mazo_cartas.append(carta)

    db.commit()
    return partida