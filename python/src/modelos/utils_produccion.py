from typing import Dict, List
import datetime

from .produccion import Produccion

# Funcion para obtener un objeto produccion
def obtenerObjetoProduccion(valores:Dict)->Produccion:

	return Produccion(fecha=valores["fecha"].strftime("%d/%m/%Y"),
					    hora=valores["hora"],
					    carbon=valores["carbon"],
					    fuel_gas=valores["fuel_gas"],
					    autoproductor=valores["autoproductor"],
					    nuclear=valores["nuclear"],
					    hidraulica=valores["hidraulica"],
					    ciclo=valores["ciclo"],
					    eolica=valores["eolica"],
					    solar_termica=valores["solar_termica"],
					    solar_fotovoltaica=valores["solar_fotovoltaica"],
					    resto=valores["resto"],
					    importacion_mibel=valores["importacion_mibel"],
					    importacion_sin_mibel=valores["importacion_sin_mibel"])

# Funcion para obtener varios objetos produccion
def obtenerObjetosProduccion(lista_valores:List[Dict])->List[Produccion]:

	return [obtenerObjetoProduccion(valor) for valor in lista_valores]