from src import crearScraper
from src.fecha import Fecha
from src.mercado import Mercado

scraper=crearScraper(Mercado("España"), Fecha(6,8,2022), Fecha(10,8,2022))

scraper.scrapear()