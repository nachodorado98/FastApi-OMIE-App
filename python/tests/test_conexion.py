import pytest
import datetime

def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_omie_data"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "prodespana" in tablas
	assert "prodportugal" in tablas
	assert "prodmibel" in tablas

def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

@pytest.mark.parametrize(["tabla"],
	[("prodespana",),("prodportugal",),("prodmibel",)]
)
def test_tabla_vacia(conexion, tabla):

	assert conexion.esta_vacia(tabla)

@pytest.mark.parametrize(["tabla"],
	[("prodespana",),("prodportugal",),("prodmibel",)]
)
def test_insertar_data_tabla(conexion, tabla):

	data=[("2019-1-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

	conexion.insertarData(tabla, data)

	conexion.c.execute(f"SELECT * FROM {tabla}")

	assert len(conexion.c.fetchall())==3

@pytest.mark.parametrize(["tabla"],
	[("prodespana",),("prodportugal",),("prodmibel",)]
)
def test_tabla_no_vacia(conexion, tabla):

	data=[("2019-1-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

	conexion.insertarData(tabla, data)

	assert not conexion.esta_vacia(tabla)

@pytest.mark.parametrize(["tabla"],
	[("prodespana",),("prodportugal",),("prodmibel",)]
)
def test_ultima_fecha_tabla_vacia(conexion, tabla):

	assert conexion.ultima_fecha(tabla) is None

@pytest.mark.parametrize(["tabla"],
	[("prodespana",),("prodportugal",),("prodmibel",)]
)
def test_ultima_fecha_fecha_unica(conexion, tabla):

	data=[("2019-1-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

	conexion.insertarData(tabla, data)

	assert conexion.ultima_fecha(tabla)==datetime.datetime(2019,1,1)

@pytest.mark.parametrize(["tabla"],
	[("prodespana",),("prodportugal",),("prodmibel",)]
)
def test_ultima_fecha_fecha_multiples(conexion, tabla):

	data=[("2019-1-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2020-1-1", 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-6-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2023-8-17", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

	conexion.insertarData(tabla, data)

	assert conexion.ultima_fecha(tabla)==datetime.datetime(2023,8,17)