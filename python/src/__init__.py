from fastapi import FastAPI
import time

from .metadata.confmetadata import *
from .routers.inicio import router_inicio
from .routers.producciones import router_producciones
from .autenticacion.auth import router_auth
from .routers.refrescar import router_refrescar

from .scraper.src_scraper import crearScraper
from .scraper.src_scraper.mercado import Mercado

# Funcion que scrapea segun el objeto creado
def scrapearData(mercado:str)->None:

	try:

		scraper=crearScraper(Mercado(mercado))

		if scraper is not None:

			scraper.scrapear()

	except AttributeError as e:

		print("Reconectando...")

		time.sleep(5)

		scrapearData(mercado)

# Funcion para crear la app
def crear_app():

	app=FastAPI(title=TITULO,
				description=DESCRIPCION,
				version=VERSION,
				contact=CONTACTO,
				license_info=LICENCIA)

	app.include_router(router_inicio)
	app.include_router(router_producciones)
	app.include_router(router_auth)
	app.include_router(router_refrescar)

	scrapearData("España")
	scrapearData("Portugal")
	scrapearData("Mibel")

	return app