from src import crearScraper
from src.mercado import Mercado

# Funcion que scrapea segun el objeto creado
def scrapearData(mercado:str)->None:

	try:

		scraper=crearScraper(Mercado(mercado))

		scraper.scrapear()

	except Exception:

		print("Tabla actualizada a fecha actual")


scrapearData("España")