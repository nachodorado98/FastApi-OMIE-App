import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List

from .confconexion import *

# Clase para la conexion a la BBDD
class Conexion:

	def __init__(self)->None:

		try:
			
			self.bbdd=psycopg2.connect(host=HOST, user=USUARIO, password=CONTRASENA, port=PUERTO, database=BBDD)
			self.c=self.bbdd.cursor(cursor_factory=RealDictCursor)

		except psycopg2.OperationalError as e:

			print("Error en la conexion a la BBDD")
			print(e)

	# Metodo para cerrar la conexion a la BBDD
	def cerrarConexion(self)->None:

		self.c.close()
		self.bbdd.close()

	# Metodo para insertar la data en la tabla
	def insertarData(self, tabla:str, data:List[tuple])->None:

		self.c.executemany(f"""INSERT INTO {tabla} 
							(fecha, hora, carbon, fuel_gas, autoproductor, nuclear, hidraulica, ciclo, eolica,
							solar_termica, solar_fotovoltaica, resto, importacion_mibel, importacion_sin_mibel)
							VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
							data)

		self.bbdd.commit()