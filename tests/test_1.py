import DeltaDB.data_processing.analysis.comparator as comp
import DeltaDB.data_processing.ingestion.ingester as ing

from tests.tools.factory import iniciar_partida

def test_iniciar_partida(test_session):
    '''Test para iniciar una partida con suficientes jugadores'''
    captura_inicial = ing.capture_all_tables(test_session)
    
    iniciar_partida(db=test_session, id_partida='1')
    
    captura_final = ing.capture_all_tables(test_session)

    captureDiff = comp.diff_captures(captura_inicial, captura_final)

    print(captureDiff.created)
    print(captureDiff.deleted)
    print(captureDiff.changes)
    assert False