import pytest
import datetime
import pandas as pd

from src.scraper import Scraper
from src.fecha import Fecha
from src.mercado import Mercado


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
def test_crear_scraper_fecha_defecto(fecha_inicio):

	scraper=Scraper(Mercado("España"), fecha_inicio)

	assert scraper.fecha_inicio.fecha_datetime<=scraper.fecha_fin.fecha_datetime
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
		(22,6,2019)
	]
)
def test_extraer_data_directamente(scraper, dia, mes, ano):

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
		(22,6,2019)
	]
)
def test_limpiar_data_directamente(scraper, dia, mes, ano):

	fecha=Fecha(dia, mes, ano)

	data=scraper._Scraper__extraerData(dia, mes, ano)

	data_limpia=scraper._Scraper__limpiarData(data)

	assert isinstance(data_limpia, list)
	assert "Fecha" in data_limpia[0]

	for registro in data_limpia[1:]:

		assert fecha.fecha_str_formato in registro
		assert isinstance(registro[1],int)

def test_extraccion_transformacion_directamente_incorrecto(scraper):

	with pytest.raises(Exception):

		scraper.__ExtraccionTransformacion("Fecha")

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(22,2,2023),
		(10,1,2021),
		(13,4,2019),
		(22,6,2019)
	]
)
def test_extraccion_transformacion_directamente(scraper, dia, mes, ano):

	fecha=Fecha(dia, mes, ano)

	data_limpia=scraper._Scraper__ExtraccionTransformacion(fecha)

	assert isinstance(data_limpia, list)
	assert "Fecha" in data_limpia[0]

	for registro in data_limpia[1:]:

		assert fecha.fecha_str_formato in registro
		assert isinstance(registro[1],int)

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(22,2,2023),
		(10,1,2021),
		(13,4,2019),
		(22,6,2019)
	]
)
def test_resultados_procesos_iguales(scraper, dia, mes, ano):

	fecha=Fecha(dia, mes, ano)

	data=scraper._Scraper__extraerData(dia, mes, ano)

	data_limpia1=scraper._Scraper__limpiarData(data)

	data_limpia2=scraper._Scraper__ExtraccionTransformacion(fecha)

	assert data_limpia1==data_limpia2

def test_crear_tabla_directamente_incorrecto(scraper):

	with pytest.raises(AttributeError):

		scraper.__crearTabla("Data")

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(22,2,2023),
		(10,1,2021),
		(13,4,2019),
		(22,6,2019)
	]
)
def test_crear_tabla_directamente(scraper, dia, mes, ano):

	fecha=Fecha(dia, mes, ano)

	data_limpia=scraper._Scraper__ExtraccionTransformacion(fecha)

	tabla=scraper._Scraper__crearTabla(data_limpia)

	assert isinstance(tabla, pd.DataFrame)

	for fila_fecha in tabla["Fecha"]:

		assert fecha.fecha_str_formato==fila_fecha

def test_scrapear(scraper):

	tabla=scraper.scrapear()

	assert tabla["Fecha"].iloc[0]==scraper.fecha_inicio.fecha_str_formato
	assert tabla["Hora"].iloc[0]==1
	assert tabla["Fecha"].iloc[-1]==scraper.fecha_fin.fecha_str_formato
	assert tabla["Hora"].iloc[-1]==24