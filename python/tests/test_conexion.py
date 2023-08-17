def test_conexion(conexion):

	conexion.c.execute("SELECT current_database();")

	assert conexion.c.fetchone()["current_database"]=="bbdd_omie_data"

	conexion.c.execute("select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';")

	tablas=[tabla["relname"] for tabla in conexion.c.fetchall()]

	assert "prodespana" in tablas

def test_cerrar_conexion(conexion):

	assert not conexion.bbdd.closed

	conexion.cerrarConexion()

	assert conexion.bbdd.closed

def test_tabla_vacia(conexion):

	conexion.c.execute("SELECT * FROM prodespana")

	assert len(conexion.c.fetchall())==0

def test_insertar_data_tabla(conexion):

	data=[("2019-1-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

	conexion.insertarData("prodespana", data)

	conexion.c.execute("SELECT * FROM prodespana")

	assert len(conexion.c.fetchall())==3

