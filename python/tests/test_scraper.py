import pytest
import datetime
import pandas as pd

from src.scraper import Scraper
from src.fecha import Fecha
from src.mercado import Mercado
from src import crearScraper


@pytest.mark.parametrize(["fecha_inicio","fecha_fin"],
	[
		(Fecha(2,1,2019), Fecha(1,1,2019)),
		(Fecha(16,8,2023), Fecha(15,8,2023)),
		(Fecha(22,6,2019), Fecha(13,4,2019))
	]

)
def test_crear_scraper_fecha_invalida(fecha_inicio, fecha_fin):

	with pytest.raises(Exception):

		Scraper(Mercado("España"), fecha_inicio, fecha_fin)

@pytest.mark.parametrize(["fecha_inicio"],
	[
		(Fecha(2,1,2019),),
		(Fecha(16,8,2023),),
		(Fecha(22,6,2019),),
		(Fecha(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year),)
	]
)
def test_crear_scraper_fecha_defecto_fin(fecha_inicio):

	scraper=Scraper(Mercado("España"), fecha_inicio)

	assert scraper.fecha_inicio.fecha_datetime<=scraper.fecha_fin.fecha_datetime
	assert scraper.fecha_fin.dia==datetime.datetime.today().day
	assert scraper.fecha_fin.mes==datetime.datetime.today().month
	assert scraper.fecha_fin.ano==datetime.datetime.today().year

def test_crear_scraper_fecha_defecto_inicio_fin():

	scraper=Scraper(Mercado("España"))

	assert scraper.fecha_inicio.dia==1
	assert scraper.fecha_inicio.mes==1
	assert scraper.fecha_inicio.ano==2019
	assert scraper.fecha_fin.dia==datetime.datetime.today().day
	assert scraper.fecha_fin.mes==datetime.datetime.today().month
	assert scraper.fecha_fin.ano==datetime.datetime.today().year

@pytest.mark.parametrize(["fecha_inicio","fecha_fin"],
	[
		(Fecha(1,1,2019), Fecha(1,1,2019)),
		(Fecha(14,8,2023), Fecha(15,8,2023)),
		(Fecha(22,6,2019), Fecha(13,4,2020))
	]

)
def test_crear_scraper_fechas_ok(fecha_inicio, fecha_fin):

	scraper=Scraper(Mercado("España"), fecha_inicio, fecha_fin)

	assert isinstance(scraper, Scraper)
	assert isinstance(scraper.fecha_inicio, Fecha)
	assert isinstance(scraper.fecha_fin, Fecha)
	assert isinstance(scraper.mercado, Mercado)

@pytest.mark.parametrize(["fecha_inicio","fecha_fin","dias"],
	[
		(Fecha(1,1,2019), Fecha(1,1,2019), 1),
		(Fecha(14,8,2023), Fecha(15,8,2023), 2),
		(Fecha(22,6,2019), Fecha(13,7,2019), 22),
		(Fecha(22,6,2019), Fecha(22,6,2020), 367),
		(Fecha(13,4,2021), Fecha(13,4,2022), 366)
	]

)
def test_crear_scraper_generar_fechas(fecha_inicio, fecha_fin, dias):

	scraper=Scraper(Mercado("España"), fecha_inicio, fecha_fin)

	assert len(scraper.fechas)==dias

def test_extraer_data_directamente_incorrecto(scraper):

	with pytest.raises(AttributeError):

		scraper.__extraerData()

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(22,2,2023),
		(10,1,2021),
		(13,4,2019),
		(22,6,2019),
		(30,7,2023),
		(6,8,2023),
		(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year)

	]
)
def test_extraer_data(scraper, dia, mes, ano):

	fecha=Fecha(dia, mes, ano)

	data=scraper._Scraper__extraerData(dia, mes, ano)

	assert isinstance(data, str)
	assert fecha.fecha_str in data

def test_limpiar_data_directamente_incorrecto(scraper):

	with pytest.raises(AttributeError):

		scraper.__limpiarData("Data")

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(22,2,2023),
		(10,1,2021),
		(13,4,2019),
		(22,6,2019),
		(30,7,2023),
		(6,8,2023),
		(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year)
	]
)
def test_limpiar_data(scraper, dia, mes, ano):

	fecha=Fecha(dia, mes, ano)

	data=scraper._Scraper__extraerData(dia, mes, ano)

	data_limpia=scraper._Scraper__limpiarData(data)

	assert isinstance(data_limpia, list)
	assert "Fecha" not in data_limpia[0]

	for registro in data_limpia:

		assert len(registro)==14
		assert fecha.fecha_str_formato in registro
		assert isinstance(registro[1],int)
		assert isinstance(registro, tuple)

def test_almacenar_data_directamente_incorrecto(scraper):

	with pytest.raises(AttributeError):

		scraper.__almacenarData("Data")

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(22,2,2023),
		(10,1,2021),
		(13,4,2019),
		(22,6,2019),
		(30,7,2023),
		(6,8,2023),
		(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year)
	]
)
def test_almacenar_data(scraper, conexion, dia, mes, ano):

	fecha=Fecha(dia, mes, ano)

	data=scraper._Scraper__extraerData(dia, mes, ano)

	data_limpia=scraper._Scraper__limpiarData(data)

	scraper._Scraper__almacenarData(data_limpia)

	conexion.c.execute(f"SELECT fecha, hora FROM {scraper.mercado.tabla} ORDER BY hora")

	registros=conexion.c.fetchall()

	assert len(registros)==24
	assert registros[0]["fecha"]==fecha.fecha_datetime.date()
	assert registros[-1]["fecha"]==fecha.fecha_datetime.date()
	assert registros[0]["hora"]==1
	assert registros[-1]["hora"]==24

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(22,2,2023),
		(10,1,2021),
		(13,4,2019),
		(22,6,2019),
		(30,7,2023),
		(6,8,2023),
		(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year)
	]
)
def test_ETL(scraper, conexion, dia, mes, ano):

	fecha=Fecha(dia, mes, ano)

	scraper.ETL(fecha)

	conexion.c.execute(f"SELECT fecha, hora FROM {scraper.mercado.tabla} ORDER BY hora")

	registros=conexion.c.fetchall()

	assert len(registros)==24
	assert registros[0]["fecha"]==fecha.fecha_datetime.date()
	assert registros[-1]["fecha"]==fecha.fecha_datetime.date()
	assert registros[0]["hora"]==1
	assert registros[-1]["hora"]==24

def test_scrapear(scraper, conexion):

	fecha_inicio=scraper.fecha_inicio.fecha_datetime.date()
	fecha_fin=scraper.fecha_fin.fecha_datetime.date()

	scraper.scrapear()

	conexion.c.execute(f"SELECT fecha, hora FROM {scraper.mercado.tabla} ORDER BY fecha, hora")

	registros=conexion.c.fetchall()

	assert len(registros)==48
	assert registros[0]["fecha"]==fecha_inicio
	assert registros[-1]["fecha"]==fecha_fin
	assert registros[0]["hora"]==1
	assert registros[-1]["hora"]==24


@pytest.mark.parametrize(["mercado"],
	[("ESPAÑA",),("PORTUGAL",),("MIBEL",)]
)
def test_crear_scraper_tabla_vacia(conexion, mercado):

	scraper=crearScraper(Mercado(mercado))

	assert scraper.fecha_inicio.dia==1
	assert scraper.fecha_inicio.mes==1
	assert scraper.fecha_inicio.ano==2019
	assert scraper.fecha_fin.dia==datetime.datetime.today().day
	assert scraper.fecha_fin.mes==datetime.datetime.today().month
	assert scraper.fecha_fin.ano==datetime.datetime.today().year
	assert scraper.mercado.mercado==mercado

@pytest.mark.parametrize(["tabla","mercado"],
	[
		("prodespana", "ESPAÑA"),
		("prodportugal", "PORTUGAL"),
		("prodmibel", "MIBEL",)
	]
)
def test_crear_scraper_tabla_llena(conexion, tabla, mercado):

	data=[("2019-1-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2020-1-1", 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-6-1", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2023-8-16", 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
			("2019-1-1", 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

	conexion.insertarData(tabla, data)

	scraper=crearScraper(Mercado(mercado))

	assert scraper.fecha_inicio.dia==17
	assert scraper.fecha_inicio.mes==8
	assert scraper.fecha_inicio.ano==2023
	assert scraper.fecha_fin.dia==datetime.datetime.today().day
	assert scraper.fecha_fin.mes==datetime.datetime.today().month
	assert scraper.fecha_fin.ano==datetime.datetime.today().year
	assert scraper.mercado.mercado==mercado

@pytest.mark.parametrize(["tabla","mercado"],
	[
		("prodespana", "ESPAÑA"),
		("prodportugal", "PORTUGAL"),
		("prodmibel", "MIBEL",)
	]
)
def test_crear_scraper_tabla_actualizada(conexion, tabla, mercado):

	fecha=Fecha(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year)

	data=[(fecha.fecha_str_formato, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)]

	conexion.insertarData(tabla, data)

	with pytest.raises(Exception):
	
		crearScraper(Mercado(mercado))