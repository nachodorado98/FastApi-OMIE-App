import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest

from src.scraper import Scraper
from src.fecha import Fecha
from src.mercado import Mercado
from src.database.conexion import Conexion

@pytest.fixture
def mercado():

	return Mercado()

@pytest.fixture
def fecha_inicio():

	return Fecha()

@pytest.fixture
def fecha_fin():

	return Fecha(2,1,2019)

@pytest.fixture
def scraper(mercado, fecha_inicio, fecha_fin):

	return Scraper(mercado, fecha_inicio, fecha_fin)

@pytest.fixture
def conexion():

	con=Conexion()

	con.c.execute("DELETE FROM prodespana")

	con.c.execute("DELETE FROM prodportugal")

	con.c.execute("DELETE FROM prodmibel")

	con.bbdd.commit()

	return con