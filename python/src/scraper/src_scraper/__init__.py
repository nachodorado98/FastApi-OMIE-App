import datetime
from typing import Optional

from .scraper import Scraper
from .fecha import Fecha
from .mercado import Mercado
from .database_scraper.conexion import Conexion

# Funcion para crear un objeto scraper segun condiciones de la BBDD
def crearScraper(mercado:Mercado)->Optional[Scraper]:

	print(mercado.mercado)

	con=Conexion()

	# Scraper desde inicio
	if con.esta_vacia(mercado.tabla):

		print("Desde inicio")

		return Scraper(mercado, Fecha(6,8,2023))

	ultima_fecha=con.ultima_fecha(mercado.tabla)

	# Scraper desde la fecha siguiente a la ultima
	if ultima_fecha.date()!=datetime.datetime.today().date():

		fecha=Fecha.desdeDatetime(ultima_fecha)

		fecha.aumentarDias(1)

		print(f"Desde {fecha.fecha_str}")

		return Scraper(mercado, fecha)

	# No hay scraper, tabla actualizada
	else:

		print("Tabla actualizada a fecha actual")
	