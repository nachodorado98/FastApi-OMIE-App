import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional, Dict
import datetime

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

	# Metodo para saber si la tabla esta vacia
	def esta_vacia(self, tabla:str)->bool:

		self.c.execute(f"""SELECT *
							FROM {tabla}""")

		return True if self.c.fetchall()==[] else False

	# Metodo para obtener la ultima fecha insertada
	def ultima_fecha(self, tabla:str)->Optional[datetime.datetime]:

		if self.esta_vacia(tabla):

			return None

		self.c.execute(f"""SELECT MAX(fecha) AS fecha_maxima
							FROM {tabla}""")

		fecha_maxima=self.c.fetchone()

		return datetime.datetime(fecha_maxima["fecha_maxima"].year, fecha_maxima["fecha_maxima"].month, fecha_maxima["fecha_maxima"].day)

	# Metodo para obtener los registros de una tabla
	def obtenerRegistros(self, tabla:str)->Optional[List[Dict]]:

		self.c.execute(f"""SELECT *
							FROM {tabla}
							ORDER BY fecha, hora""")

		registros=self.c.fetchall()

		return None if registros==[] else registros

	# Metodo para obtener los registros de una tabla con limite y salto
	def obtenerRegistrosRango(self, tabla:str, limite:int, saltar:int)->Optional[List[Dict]]:

		self.c.execute(f"""SELECT *
							FROM {tabla}
							ORDER BY fecha, hora
							LIMIT {limite}
							OFFSET {saltar}""")

		registros=self.c.fetchall()

		return None if registros==[] else registros
