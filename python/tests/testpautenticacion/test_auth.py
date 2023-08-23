import pytest

@pytest.mark.parametrize(["contrasena"],
	[("1234567892",),("123456789",),("1234",),("12345678910",),("contrasena",),("contrasena123",)]
)
def test_pagina_obtener_token_contrasena_error(cliente, contrasena):

	form=datos_form={"grant_type": "password", "username": "admin", "password": contrasena, "scope": "", "client_id": "", "client_secret": ""}

	respuesta=cliente.post("/tokens", data=form)

	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido

def test_pagina_obtener_token_autorizado(cliente):

	datos_form={"grant_type": "password", "username": "admin", "password": "contrasena1234", "scope": "", "client_id": "", "client_secret": ""}

	respuesta=cliente.post("/tokens", data=datos_form)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "access_token" in contenido
	assert "token_type" in contenido