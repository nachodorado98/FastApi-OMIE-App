import pytest

from src_scraper.mercado import Mercado

@pytest.mark.parametrize(["nombre"],
	[("espana",),(1,),("mercado",)]
)
def test_mercado_incorrecto(nombre):

	with pytest.raises(Exception):

		Mercado(nombre)

@pytest.mark.parametrize(["nombre", "numero","tabla"],
	[
		("españa",1, "prodespana"),
		("portugal",2, "prodportugal"),
		("mibel",9, "prodmibel")
	]
)
def test_mercado_correcto(nombre, numero, tabla):

	mercado=Mercado(nombre)

	assert mercado.mercado==nombre.upper()
	assert mercado.numero==numero
	assert mercado.tabla==tabla

def test_mercado_defecto(mercado):

	assert mercado.mercado=="ESPAÑA"
	assert mercado.numero==1
	assert mercado.tabla=="prodespana"