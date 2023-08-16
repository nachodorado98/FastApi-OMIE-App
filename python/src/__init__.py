from .scraper import Scraper
from .fecha import Fecha
from .mercado import Mercado

# Funcion para crear un objeto scraper
def crearScraper(mercado:str="España", dia:int=1, mes:int=1, ano:int=2019)->Scraper:

	return Scraper(Mercado(mercado), Fecha(dia, mes, ano))