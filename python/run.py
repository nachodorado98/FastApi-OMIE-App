from src import crearScraper
from src.fecha import Fecha
from src.mercado import Mercado

scraper=crearScraper(Mercado("España"), Fecha(1,1,2019), Fecha(16,1,2019))

tabla=scraper.scrapear()

print(tabla)