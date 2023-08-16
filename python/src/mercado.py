# Clase para un objeto mercado
class Mercado:

	mercados={"ESPAÑA":1, "PORTUGAL":2, "MIBEL":9}

	def __init__(self, mercado:str="ESPAÑA")->None:

		self.mercado=mercado.upper()
		self.numero=self.obtenerNumeroMercado

	# Propiedad para obtener el numero de mercado
	@property
	def obtenerNumeroMercado(self)->int:

		if self.mercado not in Mercado.mercados.keys():

			raise Exception("El mercado no existe")

		return Mercado.mercados[self.mercado]

	def __repr__(self)->str:

		return f"Mercado({self.mercado}, {self.numero})"