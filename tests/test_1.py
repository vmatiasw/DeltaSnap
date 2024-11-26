import DeltaDB.data_processing.analysis.comparator as comp
import DeltaDB.data_processing.ingestion.ingester as ing

from tests.tools.factory import crear_partida, unir_jugadores, iniciar_partida

def test_iniciar_partida(test_session):
    '''Test para iniciar una partida con suficientes jugadores'''
    captura_inicial = ing.capture_all_tables(test_session)
    
    iniciar_partida(db=test_session, id_partida='1')
    
    captura_final = ing.capture_all_tables(test_session)

    captureDiff = comp.diff_captures(captura_inicial, captura_final)

    print(captureDiff.changes.sort())
    assert captureDiff.created.remove_tables(['partids']).sort().data == {('partidas', 1): [('duracion_turno', 0, 60), ('iniciada', False, True), ('inicio_turno', '0', '2021-10-10T10:00:00Z')]}