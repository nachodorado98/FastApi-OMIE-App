import pytest
import datetime
import pandas as pd

from src.scraper import Scraper

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(30,2,2023),
		(70,1,2024),
		(1,20,2017),
		("a",8,2023),
		(-1,4,2019),
		(0,1,2020),
		(29,2,2023),
	]
)
def test_fecha_incorrecta_formato(dia, mes, ano):

	with pytest.raises(Exception):

		Scraper(dia, mes, ano)

def test_fecha_incorrecta_superior():

	manana=datetime.datetime.today()+datetime.timedelta(days=1)

	with pytest.raises(Exception):

		Scraper(manana.day, manana.month, manana.year)

@pytest.mark.parametrize(["dia","mes","ano"],
	[
		(28,2,2023),
		(31,1,2022),
		(1,10,2017),
		(6,8,2023),
		(13,4,2019),
		(22,6,2021),
		(29,2,2020),
		(datetime.datetime.today().day, datetime.datetime.today().month, datetime.datetime.today().year)
	]
)
def test_fecha_correcta(dia, mes, ano):

	assert Scraper(dia, mes, ano)

def test_fecha_defecto():

	assert Scraper()

def test_extraer_data_directamente_incorrecto():

	with pytest.raises(AttributeError):

		Scraper().__extraerData()

def test_extraer_data_directamente(objeto):

	data=objeto._Scraper__extraerData()

	assert isinstance(data, str)
	assert objeto.fecha_datetime.strftime("%d/%m/%Y") in data

def test_limpiar_data_directamente_incorrecto(objeto):

	data=objeto._Scraper__extraerData()

	with pytest.raises(AttributeError):

		Scraper().__limpiarData(data)

def test_limpiar_data_directamente(objeto):

	data=objeto._Scraper__extraerData()

	data_limpia=Scraper()._Scraper__limpiarData(data)

	assert isinstance(data_limpia, list)
	assert "Fecha" in data_limpia[0]

	for registro in data_limpia[1:]:

		assert objeto.fecha_datetime.strftime("%d/%m/%Y") in registro

def test_crear_tabla_directamente_incorrecto(objeto):

	data=objeto._Scraper__extraerData()

	data_limpia=Scraper()._Scraper__limpiarData(data)

	with pytest.raises(AttributeError):

		Scraper().__crearTabla(data_limpia)

def test_crear_tabla_directamente(objeto):

	data=objeto._Scraper__extraerData()

	data_limpia=Scraper()._Scraper__limpiarData(data)

	tabla=Scraper()._Scraper__crearTabla(data_limpia)

	assert isinstance(tabla, pd.DataFrame)

	for fila in tabla["Fecha"]:

		assert objeto.fecha_datetime.strftime("%d/%m/%Y")==fila

def test_scrapear(objeto):

	tabla=objeto.scrapear()

	assert isinstance(tabla, pd.DataFrame)
