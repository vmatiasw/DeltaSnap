
from DB.SqlAlchemyDB.models import Partida
from tests.tools.factory import crear_partida, unir_jugadores, iniciar_partida, MOCK_GMT_TIME_ZT, SEGUNDOS_TEMPORIZADOR_TURNO, N_CARTAS_FIGURA_TOTALES
from DeltaDB.capture.analysis.comparator import compare_captures
from DeltaDB.capture.ingest.ingester import capture, get_all_tables

def test_iniciar_partida_200(test_db):
    '''Test para iniciar una partida con suficientes jugadores'''

    partida = crear_partida(test_db, password="1234")
    unir_jugadores(test_db, partida, numero_de_jugadores=2)
    
    partida2 = crear_partida(test_db)
    unir_jugadores(test_db, partida2, numero_de_jugadores=2)

    captura_inicial = capture(get_all_tables(test_db))
    
    iniciar_partida(db=test_db, partida=partida)
    
    captura_final = capture(get_all_tables(test_db))

    modificaciones, eliminadas, creadas = compare_captures(captura_inicial, captura_final)
    print(modificaciones, eliminadas, creadas)
    assert False