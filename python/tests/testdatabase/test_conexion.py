import pytest

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
def test_obtener_registros_tabla_vacia(conexion, tabla):

	assert conexion.obtenerRegistros(tabla) is None

@pytest.mark.parametrize(["tabla"],
	[("prodespana",),("prodportugal",),("prodmibel",)]
)
def test_obtener_registros_tabla_llena(conexion, tabla):

	data=[("2019-1-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2020-1-1", 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-6-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2023-8-17", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

	conexion.insertarData(tabla, data)

	registros=conexion.obtenerRegistros(tabla)

	assert len(registros)==len(data)
	assert len(registros[0])==len(data[0])+1
	assert registros[-1]["fecha"]>registros[0]["fecha"]