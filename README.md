# DeltaDB
<!-- TODO: completar -->
## Que es

## Para que sirve
Usualmente, al testear la base de datos se suele hacer lo siguiente:

```python
def test_iniciar_partida(test_session):
	'''Test para iniciar una partida'''

	# Se llama a la funcionalidad

	# Se testea que se haya cambiado la base de datos como correspondia:
	partida = test_session.get(Partida, 1)
	assert partida.iniciada == True
	assert partida.iniciada == '2021-10-10T10:00:00Z'
	assert partida.iniciada == 60
```
En mi opinión este tipo de test tiene dos defectos:
1. Hay que pensar en los asserts que valen la pena chequear (ya que no se puede poner uno por cada columna de cada tabla de la db)
2. Se puede no chequear algo que si era importante chequear, y esto no necesariamente es porque se hizo mal el test, quizás algo que se agrego luego y no se actualizo en el test.

Por esta razón me parece útil una herramienta que permita sacar capturas en dos puntos (antes y después de ejecutar la funcionalidad) y compararlas para conocer que tablas se eliminaron, crearon y modificaron, y en las que se modificaron, que es lo que se modifico.
Y esa herramienta es justo la que cree y llame DeltaDB.
Un test utilizándola no solo testearia correctitud en ciertas tablas y campos arbitrarios como en el caso anterior, testearia todo, correctitud y completitud.

Ventajas:
1. El programador no elige las partes de la base de datos a testear, se testea toda.
2. Si hay que testear muchas cosas no se ocupa tantos asserts, se puede hacer todo en uno.
3. Si se actualiza el esquema de la base de datos los test se actualizan al instante y fallan si alguna funcionalidad llega a cambiar algo mas o menos de lo que cambiaba antes.
4. Se testea el valor anterior ademas. Cosa que nunca se hace.

Antes de dar un ejemplo, explicare como funciona la herramienta. Básicamente podes ejecutar en dos puntos cualquiera la función `capture_all_tables(test_session)` para obtener las capturas de la db en esos puntos, y luego con la función `diff_captures(captura_inicial, captura_final)` se obtiene los siguientes datos:
- Tablas eliminadas: conjunto de tuplas `('nombre de tabla', id de tabla)`
- Tablas creadas: conjunto de tuplas `('nombre de tabla', id de tabla)`
- Tablas modificadas: diccionario con claves de la forma `('nombre de tabla', id de tabla)` y valores de la forma de diccionario con clave `'nombre de la columna'` y valor `(valor inicial, valor final)`

Finalmente, un test quedaría así:
```python
from DeltaDB import capture_all_tables, diff_captures

def test_iniciar_partida(test_session):
	'''Test para iniciar una partida'''
	captura_inicial = capture_all_tables(test_session)
	
	# Se llama a la funcionalidad
	
	captura_final = capture_all_tables(test_session)
	changes, created, deleted = diff_captures(captura_inicial, captura_final)
	
	assert not deleted.data
	assert not created.data
	assert changes.data == {
		('partidas', 1): {
			'iniciada': (False, True),
			'inicio_turno': ('0', '2021-10-10T10:00:00Z'),
			'duracion_turno': (0, 60)}}
```

Aun así, hay muchos test que requieren de preparar una base de datos de prueba, para ello lo que habría que hacer es crear una representativa de una real pero lo mas chica posible (balancear) e irla actualizando; y que los test nunca modifiquen la base de datos de prueba (rollback).

Luego hay algunos problemas, por ejemplo que pasa si una funcionalidad no es determinista? bueno, para esos casos construí algunas herramientas para manipular los datos devueltos para analizar solo lo que queremos analizar como ignorar tablas o columnas de tablas, solo contar frecuencias, chequear esquemas,... y se pueden construir aun mas herramientas, pero por ahora eso escapa a las ganas que tengo de seguir codeando en este proyecto que actualmente a nadie sirve.

Acepto mejoras, no se si hice las mejores decisiones de diseño en las interfaces, marcas #, ...
Ademas, solo adapte para sqlalchemy en python claramente, faltaría ver para otros orms como django y sin orm,... Creería que lo único que hay que modificar para adaptar todo seria agregar en la carpeta DBMetadataAdapters el Adaptador y a db_metadata_manajer para que se elija al cambiar en la configuración ORM = 'orm elegido' por ejemplo

## Uso

## Requisitos

- Python 3.8 o superior (quizas menor, si prueban y anda cambien aca)

## Instalación

1. Clonar el repositorio.
2. Crear un entorno virtual:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Para Linux/MacOS
    venv\Scripts\activate     # Para Windows
    ```
3. Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
