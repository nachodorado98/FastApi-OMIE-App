import pytest
from typing import Dict
from fastapi.testclient import TestClient 


# Funcion para obtener el header y poder acceder
def obtenerHeaderToken(objeto_cliente:TestClient)->Dict:

	datos_form={"grant_type": "password", "username": "admin", "password": "contrasena1234", "scope": "", "client_id": "", "client_secret": ""}

	contenido_token=objeto_cliente.post("/tokens", data=datos_form).json()

	token=contenido_token["access_token"]

	return {"Authorization": f"Bearer {token}"}



@pytest.mark.parametrize(["token"],
	[("token",), ("dgfdkjg89e5yujgfkjgdf",), ("nacho98",), ("amanditaa",), ("1234",)]
)
def test_pagina_refrescar_no_autenticado(cliente, token):

	header={"Authorization": f"Bearer {token}"}

	respuesta=cliente.put("/refrescar/2023-01-01", headers=header)
	contenido=respuesta.json()

	assert respuesta.status_code==401
	assert "detail" in contenido


@pytest.mark.parametrize(["fecha"],
	[("dsfsfsd",), ("20230101",), ("122019",), ("fecha",)]
)
def test_pagina_refrescar_autenticado_fecha_formato_error(cliente, fecha):

	header=obtenerHeaderToken(cliente)

	respuesta=cliente.put(f"/refrescar/{fecha}", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido


@pytest.mark.parametrize(["fecha"],
	[("2018-01-01",), ("2010-12-06",), ("2018-12-31",)]
)
def test_pagina_refrescar_autenticado_fecha_incorrecta(cliente, fecha):

	header=obtenerHeaderToken(cliente)

	respuesta=cliente.put(f"/refrescar/{fecha}", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==400
	assert "detail" in contenido

@pytest.mark.parametrize(["fecha"],
	[("2023-08-10",), ("2023-08-16",), ("2023-08-22",)]
)
def test_pagina_refrescar_autenticado(cliente, conexion_simple, fecha):

	header=obtenerHeaderToken(cliente)

	numero_registros=len(conexion_simple.obtenerRegistros("prodespana"))

	respuesta=cliente.put(f"/refrescar/{fecha}", headers=header)

	contenido=respuesta.json()

	assert respuesta.status_code==200
	assert "mensaje" in contenido
	assert len(conexion_simple.obtenerRegistros("prodespana"))==numero_registros

	
