def test_pagina_inicio(conexion, cliente):

	contenido=cliente.get("/").json()

	assert "mensaje" in contenido
	assert "version" in contenido
	assert "descripcion" in contenido
	assert "documentacion" in contenido
