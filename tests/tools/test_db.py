from tests.tools.db.database_connector import db_connection_adapter as db_connection
from tests.tools.factory import crear_partida, unir_jugadores

session = db_connection.get_new_session()

def setup_test_db():
    '''
    Función para crear una base de datos de prueba representativa de una real.
    '''
    partida = crear_partida(session)
    unir_jugadores(session, partida, numero_de_jugadores=2)
    
    partida2 = crear_partida(session)
    unir_jugadores(session, partida2, numero_de_jugadores=2)
    
    session.commit()
