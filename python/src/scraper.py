import datetime
import requests
from typing import List
import pandas as pd

from .fecha import Fecha
from .mercado import Mercado

# Clase para scrapear
class Scraper:

	def __init__(self, mercado:Mercado, fecha:Fecha)->None:

		self.mercado=mercado
		self.fecha=fecha

	# Metodo para extraer la data de la peticion
	def __extraerData(self)->str:

		url=f"""https://www.omie.es/sites/default/files/dados/AGNO_{self.fecha.ano}/MES_{self.fecha.mes:02d}/TXT/INT_PBC_TECNOLOGIAS_H_{self.mercado.numero}_{self.fecha.dia:02d}_{self.fecha.mes:02d}_{self.fecha.ano}_{self.fecha.dia:02d}_{self.fecha.mes:02d}_{self.fecha.ano}.TXT"""

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

		print(self.fecha.fecha_str)

		data=self.__extraerData()

		data_limpia=self.__limpiarData(data)

		return self.__crearTabla(data_limpia)