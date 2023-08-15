from .scraper import Scraper

# Funcion para crear un objeto scraper
def crearScraper(dia:int=1, mes:int=1, ano:int=2019)->Scraper:

	return Scraper(dia, mes, ano)