import datetime
import requests
from typing import List
import pandas as pd

from .fecha import Fecha
from .mercado import Mercado

# Clase para scrapear
class Scraper:

	def __init__(self,
				mercado:Mercado,
				fecha_inicio:Fecha,
				fecha_fin:Fecha=Fecha(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year)
				)->None:

		self.mercado=mercado

		if fecha_inicio.fecha_datetime>fecha_fin.fecha_datetime:

			raise Exception("Fechas incorrectas")

		self.fecha_inicio=fecha_inicio
		self.fecha_fin=fecha_fin
		self.fechas=self.generarFechas

	# Metodo para generar las fechas
	@property
	def generarFechas(self)->List[Fecha]:

		fechas=[]

		dias=0

		inicio=self.fecha_inicio.fecha_datetime

		while inicio<=self.fecha_fin.fecha_datetime:

			# Creamos el objeto fecha desde datetime y lo agregamos
			fechas.append(Fecha.desdeDatetime(inicio))

			dias+=1

			inicio=self.fecha_inicio.fecha_datetime+datetime.timedelta(days=dias)

		return fechas

	# Metodo para extraer la data de la peticion
	def __extraerData(self, dia:int, mes:int, ano:int)->str:

		url=f"""https://www.omie.es/sites/default/files/dados/AGNO_{ano}/MES_{mes:02d}/TXT/INT_PBC_TECNOLOGIAS_H_{self.mercado.numero}_{dia:02d}_{mes:02d}_{ano}_{dia:02d}_{mes:02d}_{ano}.TXT"""

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

		# Eliminacion del 0 del final de la cabecera
		fila_cabecera=filas_cambiadas[0][:-1]

		# Funcion para limpiar los formatos de la fila
		def limpiarFormatosFila(lista:List)->List:

			fecha_datetime=datetime.datetime.strptime(lista[0], "%d/%m/%Y")

			# Fecha cambio de formato
			fecha=fecha_datetime.strftime("%Y-%m-%d")

			# Hora a entero
			hora=int(lista[1])

			# Eliminacion de cero y cambio de comas por puntos pasando a float
			resto=[float(str(valor).replace(".","").replace(",",".")) for valor in lista[2:-1]]

			return [fecha, hora]+resto

		filas=list(map(limpiarFormatosFila, filas_cambiadas[1:]))

		filas_definitivas=[fila_cabecera]+filas

		return filas_definitivas

	# Metodo para el proceso de extracion y transformacion de una fecha
	def __ExtraccionTransformacion(self, fecha:Fecha)->List[List]:

		print(fecha.fecha_str)

		data=self.__extraerData(fecha.dia, fecha.mes, fecha.ano)

		return self.__limpiarData(data)

	# Metodo para crear la tabla
	def __crearTabla(self, data_limpia:List[List])->pd.DataFrame:

		return pd.DataFrame(data_limpia[1:], columns=data_limpia[0])

	# Metodo para scrapear la data
	def scrapear(self)->pd.DataFrame:

		tablas=[]

		for fecha in self.fechas:

			data_limpia=self.__ExtraccionTransformacion(fecha)

			tabla=self.__crearTabla(data_limpia)

			tablas.append(tabla)

		return pd.concat(tablas)