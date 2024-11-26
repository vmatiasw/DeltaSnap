
from tests.tools.factory import crear_partida, unir_jugadores, iniciar_partida
import DeltaDB.data_processing.analysis.comparator as comp
import DeltaDB.data_processing.ingestion.ingester as ing

def test_iniciar_partida(test_db):
    '''Test para iniciar una partida con suficientes jugadores'''

    partida = crear_partida(test_db, password="1234")
    unir_jugadores(test_db, partida, numero_de_jugadores=2)
    
    partida2 = crear_partida(test_db)
    unir_jugadores(test_db, partida2, numero_de_jugadores=2)

    captura_inicial = ing.capture_all_tables(test_db)
    
    iniciar_partida(db=test_db, partida=partida)
    
    captura_final = ing.capture_all_tables(test_db)

    captureDiff = comp.diff_captures(captura_inicial, captura_final)

    print(captureDiff.changes.sort())
    assert captureDiff.created.remove_tables(['partids']).sort().data == {('partidas', 1): [('duracion_turno', 0, 60), ('iniciada', False, True), ('inicio_turno', '0', '2021-10-10T10:00:00Z')]}