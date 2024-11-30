import DeltaDB.data_processing.analysis as comp
import DeltaDB.data_processing.ingestion as ing

from tests.db.GameFactory import GameFactory

def test_iniciar_partida(test_session):
    '''Test para iniciar una partida con suficientes jugadores'''
    game = GameFactory(test_session)
    
    partida = test_session.get('Partida', 1)
    
    captura_inicial = ing.capture_all_tables(test_session)
    
    assert captura_inicial == {('jugadores', 1): {'id': 1, 'nombre': 'Creador', 'es_creador': True, 'id_partida (FK)': 1, 'orden': 0}, ('jugadores', 2): {'id': 2, 'nombre': 'Jugador2', 'es_creador': False, 'id_partida (FK)': 1, 'orden': 1}, ('jugadores', 3): {'id': 3, 'nombre': 'Jugador3', 'es_creador': False, 'id_partida (FK)': 1, 'orden': 2}, ('jugadores', 4): {'id': 4, 'nombre': 'Creador', 'es_creador': True, 'id_partida (FK)': 2, 'orden': 0}, ('jugadores', 5): {'id': 5, 'nombre': 'Jugador2', 'es_creador': False, 'id_partida (FK)': 2, 'orden': 1}, ('jugadores', 6): {'id': 6, 'nombre': 'Jugador3', 'es_creador': False, 'id_partida (FK)': 2, 'orden': 2}, ('partidas', 1): {'id': 1, 'nombre_partida': 'Partida', 'nombre_creador': 'Creador', 'iniciada': False, 'inicio_turno': '0', 'duracion_turno': 0, 'tablero': '[[2, 1, 3, 4, 2, 3], [4, 2, 1, 1, 3, 3], [2, 1, 3, 2, 3, 4], [4, 1, 1, 2, 2, 4], [1, 3, 1, 2, 1, 3], [2, 3, 4, 4, 4, 4]]'}, ('partidas', 2): {'id': 2, 'nombre_partida': 'Partida', 'nombre_creador': 'Creador', 'iniciada': False, 'inicio_turno': '0', 'duracion_turno': 0, 'tablero': '[[2, 1, 3, 4, 2, 3], [4, 2, 1, 1, 3, 3], [2, 1, 3, 2, 3, 4], [4, 1, 1, 2, 2, 4], [1, 3, 1, 2, 1, 3], [2, 3, 4, 4, 4, 4]]'}}
    
    game.iniciar_partida(partida)
    
    captura_final = ing.capture_all_tables(test_session)
    
    assert captura_final != captura_inicial

    captureDiff = comp.diff_captures(captura_inicial, captura_final)

    assert captureDiff.created.data == {('cartas', 5), ('cartas', 4), ('cartas', 1), ('cartas', 3), ('cartas', 6), ('cartas', 2)}
    assert not captureDiff.deleted.data
    assert captureDiff.changes.data == {('partidas', 1): {'iniciada': (False, True), 'inicio_turno': ('0', '2021-10-10T10:00:00Z'), 'duracion_turno': (0, 60)}}
    assert captureDiff.created.get_frequency() == {'cartas': 6}
    assert not captureDiff.deleted.get_frequency()
    assert captureDiff.changes.get_frequency() == {'partidas': {'#table frequency': 1, 'iniciada': 1, 'inicio_turno': 1, 'duracion_turno': 1}}
    assert captureDiff.changes.ignore_diff_fields({'partidas': ['iniciada']}).data == {('partidas', 1): {'iniciada': ('#ignored', '#ignored'), 'inicio_turno': ('0', '2021-10-10T10:00:00Z'), 'duracion_turno': (0, 60)}}
    assert captureDiff.created.matches_schema({'cartas'})
    assert captureDiff.deleted.matches_schema(set())
    assert captureDiff.changes.matches_schema({('partidas', 1): {'iniciada', 'inicio_turno', 'duracion_turno'}})
    assert not captureDiff.created.remove_tables(['cartas']).data
    assert not captureDiff.deleted.remove_tables(['cartas']).data
    assert not captureDiff.changes.remove_tables(['partidas']).data