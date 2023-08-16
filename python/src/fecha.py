import datetime
from typing import Type

# Clase de un objeto fecha
class Fecha:

	def __init__(self, dia:int=1, mes:int=1, ano:int=2019)->None:

		self.fecha_datetime=self.convertirDatetime(dia,mes,ano)
		self.dia=self.fecha_datetime.day
		self.mes=self.fecha_datetime.month
		self.ano=self.fecha_datetime.year
		self.fecha_str=self.fecha_datetime.strftime("%d/%m/%Y")
		self.fecha_str_formato=self.fecha_datetime.strftime("%Y-%m-%d")

	# Metodo para convertir la fecha a un datetime
	def convertirDatetime(self, dia:int, mes:int, ano:int)->datetime.datetime:

		try:

			fecha_datetime=datetime.datetime(ano, mes, dia)

			if fecha_datetime>datetime.datetime.today() or fecha_datetime<datetime.datetime(2019,1,1):

				raise Exception("La fecha es erronea")

			return fecha_datetime

		except ValueError as e:

			raise Exception("La fecha es erronea")

	# Metodo para crear un objeto fecha desde un datetime
	@classmethod
	def desdeDatetime(cls:Type['Fecha'], fecha_datetime:datetime.datetime)->Type['Fecha']:

		return cls(fecha_datetime.day, fecha_datetime.month, fecha_datetime.year)

	def __repr__(self)->str:

		return f"Fecha({self.dia}, {self.mes}, {self.ano})"