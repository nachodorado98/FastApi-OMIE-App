import pytest

from src.mercado import Mercado

@pytest.mark.parametrize(["nombre"],
	[("espana",),(1,),("mercado",)]
)
def test_mercado_incorrecto(nombre):

	with pytest.raises(Exception):

		Mercado(nombre)

@pytest.mark.parametrize(["nombre", "numero"],
	[("españa",1),("portugal",2),("mibel",9)]
)
def test_mercado_correcto(nombre, numero):

	mercado=Mercado(nombre)

	assert mercado.numero==numero

def test_mercado_defecto(mercado):

	assert mercado.numero==1