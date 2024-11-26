from tests.tools.db.db_setup import localSession
from tests.tools.factory import crear_partida, unir_jugadores

session = localSession()

# NOTE: si se cambia esta función, se debe eliminar la base de datos de prueba.
def setup_test_db():
    '''
    Función para crear una base de datos de prueba representativa de una real.
    '''
    partida = crear_partida(session, password="1234")
    unir_jugadores(session, partida, numero_de_jugadores=2)
    
    partida2 = crear_partida(session)
    unir_jugadores(session, partida2, numero_de_jugadores=2)
    
    session.commit()
