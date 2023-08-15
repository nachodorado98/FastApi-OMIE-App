import os
import sys
sys.path.append(os.path.abspath(".."))

import pytest

from src.scraper import Scraper

@pytest.fixture
def objeto():

	return Scraper()