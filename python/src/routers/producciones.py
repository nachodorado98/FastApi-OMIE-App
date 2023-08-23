from fastapi import APIRouter, status, Path, Depends, HTTPException, Query
from typing import List

from src.scraper.src_scraper.database_scraper.conexion import Conexion
from src.scraper.src_scraper.database_scraper.sesion import crearConexion

from src.scraper.src_scraper.mercado import Mercado

from src.modelos.produccion import Produccion
from src.modelos.utils_produccion import obtenerObjetosProduccion


router_producciones=APIRouter(prefix="/producciones", tags=["Producciones"])


@router_producciones.get("/{mercado}", status_code=status.HTTP_200_OK, summary="Devuelve las producciones del mercado")
async def obtenerProducciones(mercado:str=Path(..., title="Nombre del mercado", description="El nombre del mercado para obtener sus datos"),
								todo:bool=Query(False, description="Bool para obtener todos los registros"),
								saltar:int=Query(0, description="Numero de elementos para saltar", min=0),
                    			limite:int=Query(24, description="Numero de elementos a obtener", min=1, max=100),
								con:Conexion=Depends(crearConexion))->List[Produccion]:

	"""
	Devuelve los diccionarios asociados a los datos de las producciones del mercado disponibles en la BBDD.

	## Parametros Path

	- **Mercado**: El nombre del mercado (str).

	## Parametros Query

	- **Todo**: El booleano para obtener todos los registros (bool).
	- **Saltar**: El numero de registros que quieres saltar (int).
	- **Limite**: El numero de registros limite que quieres obtener (int).

	## Respuesta

	200 (OK): Si se obtienen los datos del mercado correctamente

	- **Fecha**: La fecha de la produccion con formato dd/mm/yyyy (str).
	- **Hora**: La hora de la produccion (int).
	- **Carbon**: El campo carbon de la produccion (float).
	- **Fuel_gas**: El campo fuel gas de la produccion (float).
	- **Autoproductor**: El campo autoproductor de la produccion (float).
	- **Nuclear**: El campo nuclear de la produccion (float).
	- **Eolica**: El campo eolica de la produccion (float).
	- **Solar_termica**: El campo solar termica de la produccion (float).
	- **Solar_fotovoltaica**: El campo solar fotovoltaica de la produccion (float).
	- **Resto**: El campo resto de la produccion (float).
	- **Importacion_mibel**: El campo importacion mibel de la produccion (float).
	- **Importacion_sin_mibel**: El campo importacion sin mibel de la produccion (float).

	404 (NOT FOUND): Si no se obtienen los datos del mercado correctamente

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	try:

		tabla_mercado=Mercado(mercado).tabla

	except Exception:

		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mercado no existente")

	if todo:

		registros=con.obtenerRegistros(tabla_mercado)

	else:

		registros=con.obtenerRegistrosRango(tabla_mercado, limite, saltar)

	return obtenerObjetosProduccion(registros)