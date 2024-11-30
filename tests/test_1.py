import DeltaDB.data_processing.analysis as comp
import DeltaDB.data_processing.ingestion as ing

from tests.db.GameFactory import GameFactory
from tests.db.DBTransaction.db_transaction_manajer import DBTransaction

def test_iniciar_partida(test_session):
    '''Test para iniciar una partida con suficientes jugadores'''
    game = GameFactory(test_session)
    db = DBTransaction(test_session)
    
    partida = db.get('Partida', 1)
    
    captura_inicial = ing.capture_all_tables(test_session)
    
    assert captura_inicial == {('jugadores', 1): {'id': 1, 'nombre': 'Creador', 'es_creador': True, 'id_partida (FK)': 1, 'orden': 0}, ('jugadores', 2): {'id': 2, 'nombre': 'Jugador2', 'es_creador': False, 'id_partida (FK)': 1, 'orden': 2}, ('jugadores', 3): {'id': 3, 'nombre': 'Jugador3', 'es_creador': False, 'id_partida (FK)': 1, 'orden': 2}, ('jugadores', 4): {'id': 4, 'nombre': 'Creador', 'es_creador': True, 'id_partida (FK)': 2, 'orden': 0}, ('jugadores', 5): {'id': 5, 'nombre': 'Jugador2', 'es_creador': False, 'id_partida (FK)': 2, 'orden': 2}, ('jugadores', 6): {'id': 6, 'nombre': 'Jugador3', 'es_creador': False, 'id_partida (FK)': 2, 'orden': 2}, ('partidas', 1): {'id': 1, 'nombre_partida': 'Partida', 'nombre_creador': 'Creador', 'iniciada': False, 'inicio_turno': '0', 'duracion_turno': 0, 'tablero': '[[2, 1, 3, 4, 2, 3], [4, 2, 1, 1, 3, 3], [2, 1, 3, 2, 3, 4], [4, 1, 1, 2, 2, 4], [1, 3, 1, 2, 1, 3], [2, 3, 4, 4, 4, 4]]'}, ('partidas', 2): {'id': 2, 'nombre_partida': 'Partida', 'nombre_creador': 'Creador', 'iniciada': False, 'inicio_turno': '0', 'duracion_turno': 0, 'tablero': '[[2, 1, 3, 4, 2, 3], [4, 2, 1, 1, 3, 3], [2, 1, 3, 2, 3, 4], [4, 1, 1, 2, 2, 4], [1, 3, 1, 2, 1, 3], [2, 3, 4, 4, 4, 4]]'}}
    
    game.iniciar_partida(partida)
    
    captura_final = ing.capture_all_tables(test_session)
    
    assert captura_final != captura_inicial

    captureDiff = comp.diff_captures(captura_inicial, captura_final)

    print(captureDiff.created)
    print(captureDiff.deleted)
    print(captureDiff.changes)
    print(captureDiff.created.get_frequency())
    print(captureDiff.deleted.get_frequency())
    print(captureDiff.changes.get_frequency())
    print(captureDiff.changes.ignore_diff_fields({'partidas': ['iniciada']}))
    print(captureDiff.created.matches_schema({'cartas'}))
    print(captureDiff.deleted.matches_schema(set()))
    print(captureDiff.changes.matches_schema({('partidas', 1): {'iniciada', 'inicio_turno', 'duracion_turno'}}))
    print(captureDiff.created.remove_tables(['cartas']))
    print(captureDiff.deleted.remove_tables(['cartas']))
    print(captureDiff.changes.remove_tables(['partidas']))
    assert False