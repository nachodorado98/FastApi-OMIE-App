import datetime
import requests
from typing import List
import pandas as pd

# Clase para scrapear
class Scraper:

	def __init__(self, dia:int=1, mes:int=1, ano:int=2019)->None:

		self.fecha_datetime=self.convertirDatetime(dia,mes,ano)
		self.dia=self.fecha_datetime.day
		self.mes=self.fecha_datetime.month
		self.ano=self.fecha_datetime.year
		self.pais=1

	# Metodo para convertir la fecha a un datetime
	def convertirDatetime(self, dia:int, mes:int, ano:int)->datetime.datetime:

		try:

			fecha_datetime=datetime.datetime(ano, mes, dia)

			if fecha_datetime>datetime.datetime.today():

				raise Exception("La fecha es erronea")

			return fecha_datetime

		except ValueError as e:

			raise Exception("La fecha es erronea")

	# Metodo para extraer la data de la peticion
	def __extraerData(self)->str:

		url=f"""https://www.omie.es/sites/default/files/dados/AGNO_{self.ano}/MES_{self.mes:02d}/TXT/INT_PBC_TECNOLOGIAS_H_{self.pais}_{self.dia:02d}_{self.mes:02d}_{self.ano}_{self.dia:02d}_{self.mes:02d}_{self.ano}.TXT"""

		peticion=requests.get(url)

		if peticion.status_code!=200:

			raise Exception("Problema con la conexion con el servidor")

		data=peticion.text

		return data

	# Metodo para limpiar la data
	def __limpiarData(self, data:str)->List[List]:

		contenido=data.split("(MWh);;;;")[1].split("\r\n\r\n")[1]

		filas=contenido.split("\r\n")

		# Cambio de espacio en blanco por cero
		filas_cambiadas=[[j if j!="" else 0 for j in i.split(";")] for i in filas[:-2]]

		# Eliminacion del 0 del final
		return [fila[:-1] for fila in filas_cambiadas]

	# Metodo para crear la tabla
	def __crearTabla(self, data_limpia:List[List])->pd.DataFrame:

		tabla=pd.DataFrame(data_limpia[1:], columns=data_limpia[0])

		for columna in tabla.columns[2:]:

			#Cambio de comas por puntos
			tabla[columna]=tabla[columna].apply(lambda x: float(str(x).replace(".","").replace(",",".")))

		return tabla

	# Metodo para scrapear la data
	def scrapear(self)->pd.DataFrame:

		print(self.fecha_datetime.strftime("%d/%m/%Y"))

		data=self.__extraerData()

		data_limpia=self.__limpiarData(data)

		return self.__crearTabla(data_limpia)