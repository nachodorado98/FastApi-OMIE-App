import pytest
import datetime

@pytest.mark.parametrize(["mercado_error"],
	[("espana",),("mercado",),("gghffh",)]
)
def test_pagina_obtener_producciones_incorrecto(cliente, mercado_error):

	respuesta=cliente.get(f"/producciones/{mercado_error}")

	contenido=respuesta.json()

	assert respuesta.status_code==404
	assert "detail" in contenido

@pytest.mark.parametrize(["mercado"],
	[("españa",),("portugal",),("mibel",)]
)
def test_pagina_obtener_producciones(cliente, mercado):

	respuesta=cliente.get(f"/producciones/{mercado}")

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "fecha" in contenido[0]
	assert "hora" in contenido[0]
	assert contenido[0]["fecha"]=="06/08/2023" or contenido[0]["fecha"]=="01/01/2019"
	assert contenido[0]["hora"]==1
	assert contenido[-1]["fecha"]==datetime.datetime.today().strftime("%d/%m/%Y")
	assert contenido[-1]["hora"]==24
	assert contenido[-1]["fecha"]>contenido[0]["fecha"]
	assert contenido[-1]["hora"]>contenido[0]["hora"]
