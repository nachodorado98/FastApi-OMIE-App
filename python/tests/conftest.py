import os
import sys
sys.path.append("..")

import pytest
from fastapi.testclient import TestClient 

from src import crear_app
from src.scraper.src_scraper.database_scraper.conexion import Conexion

@pytest.fixture()
def app():

	app=crear_app()

	return app

@pytest.fixture()
def cliente(app):

	return TestClient(app)

@pytest.fixture
def conexion():

	con=Conexion()

	con.c.execute("DELETE FROM prodespana")

	con.c.execute("DELETE FROM prodportugal")

	con.c.execute("DELETE FROM prodmibel")

	con.bbdd.commit()

	return con