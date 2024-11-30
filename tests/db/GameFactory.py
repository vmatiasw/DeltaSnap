from sqlalchemy.orm import Session

from tests.db.models.sql_alchemy import Partida, Jugador, Carta

MOCK_GMT_TIME_ZT = "2021-10-10T10:00:00Z"
SEGUNDOS_TEMPORIZADOR_TURNO = 60
N_CARTAS_FIGURA_TOTALES = 6


class GameFactory:
    def __init__(self, session: Session):
        self.session = session

    def crear_partida(self) -> Partida:
        """Crea una partida inicial con un creador y la agrega a la base de datos."""
        partida = Partida(nombre_partida="Partida",
                          nombre_creador="Creador",
                          iniciada=False,
                          tablero='[[2, 1, 3, 4, 2, 3], [4, 2, 1, 1, 3, 3], [2, 1, 3, 2, 3, 4], [4, 1, 1, 2, 2, 4], [1, 3, 1, 2, 1, 3], [2, 3, 4, 4, 4, 4]]')
        
        creador = Jugador(nombre="Creador",
                          partidas=partida,
                          es_creador=True,
                          orden=0)
        partida.jugadores.append(creador)

        self.session.add(creador)
        self.session.add(partida)
        self.session.flush()  # Asegúrate de hacer flush para persistir en la base de datos
        return partida

    def unir_jugadores(self, partida: Partida, numero_de_jugadores: int = 1) -> list[Jugador]:
        """Agrega jugadores a una partida existente."""
        assert partida.iniciada == False, "La partida ya ha sido iniciada"
        assert len(partida.jugadores) <= 4, "La partida ya tiene 4 jugadores"
        assert len(partida.jugadores) > 0, "Y el creador? boludito"
        assert numero_de_jugadores < 4, "No se pueden unir más de 4 jugadores a la partida"

        if numero_de_jugadores == 0:
            return []

        nuevos_jugadores = []
        for i in range(numero_de_jugadores):
            nuevo_jugador = Jugador(
                nombre=f"Jugador{i+2}", partidas=partida, es_creador=False, orden=len(partida.jugadores))
            self.session.add(nuevo_jugador)
            partida.jugadores.append(nuevo_jugador)
            nuevos_jugadores.append(nuevo_jugador)
            self.session.commit()  # Commit para persistir los nuevos jugadores

        self.session.flush()
        return nuevos_jugadores

    def iniciar_partida(self, partida: Partida) -> Partida:
        """Inicia una partida, reparte cartas y actualiza el estado de la partida."""
        assert partida.iniciada == False, "La partida ya ha sido iniciada"
        assert len(partida.jugadores) > 1, "La partida debe tener al menos 2 jugadores para poder iniciarla"
        assert len(partida.jugadores) <= 4, "La partida no puede tener más de 4 jugadores"

        partida.iniciada = True
        partida.inicio_turno = MOCK_GMT_TIME_ZT
        partida.duracion_turno = SEGUNDOS_TEMPORIZADOR_TURNO

        numero_de_cartas_por_jugador = int(N_CARTAS_FIGURA_TOTALES / len(partida.jugadores))
        self.__repartir_cartas(partida, 3, numero_de_cartas_por_jugador)

        self.session.flush()
        return partida

    def __repartir_cartas(self, partida: Partida, n_cartas_reveladas: int, n_cartas_por_jugador: int):
        """Reparte las cartas entre los jugadores de una partida."""
        assert n_cartas_por_jugador <= int(N_CARTAS_FIGURA_TOTALES / len(partida.jugadores))
        assert partida.iniciada == True, "La partida no ha sido iniciada"
        assert len(partida.jugadores) > 1, "La partida debe tener al menos 2 jugadores para poder repartir las cartas de figura"
        assert len(partida.jugadores) <= 4, "La partida no puede tener más de 4 jugadores"

        # Crear las cartas de figura
        for jugador in partida.jugadores:
            for i in range(n_cartas_por_jugador - len(jugador.mazo_cartas)):
                carta = Carta(poseida_por=jugador,
                              revelada=(i < n_cartas_reveladas))
                self.session.add(carta)
                jugador.mazo_cartas.append(carta)

        self.session.flush()
        