import os
import sys
sys.path.append("..")

import pytest
from fastapi.testclient import TestClient 

from src import crear_app

@pytest.fixture()
def app():

	app=crear_app()

	return app


@pytest.fixture()
def cliente(app):

	return TestClient(app)