import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest

from src.scraper import Scraper
from src.fecha import Fecha
from src.mercado import Mercado

@pytest.fixture
def mercado():

	return Mercado()

@pytest.fixture
def fecha():

	return Fecha()

@pytest.fixture
def scraper(mercado, fecha):

	return Scraper(mercado, fecha)