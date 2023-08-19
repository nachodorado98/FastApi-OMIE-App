import datetime

from src.modelos.produccion import Produccion
from src.modelos.utils_produccion import obtenerObjetoProduccion, obtenerObjetosProduccion

def test_obtener_produccion():

	fecha=datetime.date(2023, 8, 6)

	produccion={"id":1,"fecha":fecha,"hora":1,"carbon":0.0,"fuel_gas":0.0,"autoproductor":0.0,"nuclear":0.0,"hidraulica":325.5,"ciclo":295.0,"eolica":1464.9,
			"solar_termica":0.0,"solar_fotovoltaica":0.0,"resto":593.8,"importacion_mibel":0.0,"importacion_sin_mibel":3051.4}

	objeto=obtenerObjetoProduccion(produccion)

	assert isinstance(objeto, Produccion)
	assert objeto.fecha==fecha.strftime("%d/%m/%Y")
	assert "id" not in objeto

def test_obtener_varios_produccion():

	fecha=datetime.date(2023, 8, 6)

	producciones=[{"id":1,"fecha":fecha,"hora":1,"carbon":0.0,"fuel_gas":0.0, "autoproductor":0.0,"nuclear":0.0,"hidraulica":325.5,"ciclo":295.0,"eolica":1464.9,
				"solar_termica":0.0,"solar_fotovoltaica":0.0,"resto":593.8,"importacion_mibel":0.0,"importacion_sin_mibel":3051.4},
				{"id":2,"fecha":fecha,"hora":1,"carbon":0.0,"fuel_gas":0.0, "autoproductor":0.0,"nuclear":0.0,"hidraulica":325.5,"ciclo":295.0,"eolica":1464.9,
				"solar_termica":0.0,"solar_fotovoltaica":0.0,"resto":593.8,"importacion_mibel":0.0,"importacion_sin_mibel":3051.4},
				{"id":3,"fecha":fecha,"hora":1,"carbon":0.0,"fuel_gas":0.0, "autoproductor":0.0,"nuclear":0.0,"hidraulica":325.5,"ciclo":295.0,"eolica":1464.9,
				"solar_termica":0.0,"solar_fotovoltaica":0.0,"resto":593.8,"importacion_mibel":0.0,"importacion_sin_mibel":3051.4}]

	objetos=obtenerObjetosProduccion(producciones)

	assert len(objetos)==3

	for objeto in objetos:

		assert isinstance(objeto, Produccion)
		assert objeto.fecha==fecha.strftime("%d/%m/%Y")
		assert "id" not in objeto
