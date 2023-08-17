# Clase para un objeto mercado
class Mercado:

	data_mercados={"ESPAÑA":{"numero":1, "tabla":"prodespana"}, 
					"PORTUGAL":{"numero":2, "tabla":"prodportugal"},
					"MIBEL":{"numero":9, "tabla":"prodmibel"}}

	def __init__(self, mercado:str="ESPAÑA")->None:

		self.mercado=mercado.upper()
		self.numero=self.obtenerNumeroMercado
		self.tabla=self.obtenerTabla

	# Propiedad para obtener el numero de mercado
	@property
	def obtenerNumeroMercado(self)->int:

		if self.mercado not in Mercado.data_mercados.keys():

			raise Exception("El mercado no existe")

		return Mercado.data_mercados[self.mercado]["numero"]

	# Propiedad para obtener el nombre de la tabla
	@property
	def obtenerTabla(self)->int:

		return Mercado.data_mercados[self.mercado]["tabla"]

	def __repr__(self)->str:

		return f"Mercado({self.mercado}, {self.numero})"