from .scraper import Scraper
from .fecha import Fecha
from .mercado import Mercado

# Funcion para crear un objeto scraper
def crearScraper(mercado:Mercado, fecha_inicio:Fecha, fecha_fin:Fecha=None)->Scraper:

	if fecha_fin is None:

		return Scraper(mercado, fecha_inicio)

	return Scraper(mercado, fecha_inicio, fecha_fin)	