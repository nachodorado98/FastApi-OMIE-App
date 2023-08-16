import pytest
import datetime
import pandas as pd

from src.scraper import Scraper
from src.fecha import Fecha
from src.mercado import Mercado

def test_crear_objeto_scraper(scraper):

	assert isinstance(scraper, Scraper)
	assert isinstance(scraper.fecha, Fecha)
	assert isinstance(scraper.mercado, Mercado)

def test_extraer_data_directamente_incorrecto(scraper):

	with pytest.raises(AttributeError):

		scraper.__extraerData()

def test_extraer_data_directamente(scraper):

	data=scraper._Scraper__extraerData()

	assert isinstance(data, str)
	assert scraper.fecha.fecha_str in data

def test_limpiar_data_directamente_incorrecto(scraper):

	data=scraper._Scraper__extraerData()

	with pytest.raises(AttributeError):

		scraper.__limpiarData(data)

def test_limpiar_data_directamente(scraper):

	data=scraper._Scraper__extraerData()

	data_limpia=scraper._Scraper__limpiarData(data)

	assert isinstance(data_limpia, list)
	assert "Fecha" in data_limpia[0]

	for registro in data_limpia[1:]:

		assert scraper.fecha.fecha_str in registro

def test_crear_tabla_directamente_incorrecto(scraper):

	data=scraper._Scraper__extraerData()

	data_limpia=scraper._Scraper__limpiarData(data)

	with pytest.raises(AttributeError):

		scraper.__crearTabla(data_limpia)

def test_crear_tabla_directamente(scraper):

	data=scraper._Scraper__extraerData()

	data_limpia=scraper._Scraper__limpiarData(data)

	tabla=scraper._Scraper__crearTabla(data_limpia)

	assert isinstance(tabla, pd.DataFrame)

	for fila in tabla["Fecha"]:

		assert scraper.fecha.fecha_datetime.strftime("%d/%m/%Y")==fila

def test_scrapear(scraper):

	tabla=scraper.scrapear()

	assert isinstance(tabla, pd.DataFrame)
