from fastapi import APIRouter, status, Depends, HTTPException, Path
from typing import Dict
import datetime

from src.scraper.src_scraper.database_scraper.conexion import Conexion
from src.scraper.src_scraper.database_scraper.sesion import crearConexion

from src.modelos.token import Payload

from src.autenticacion.utils_auth import decodificarToken

from src.scraper.src_scraper.fecha import Fecha
from src.scraper.src_scraper.mercado import Mercado
from src.scraper.src_scraper import crearScraper


router_refrescar=APIRouter(prefix="/refrescar", tags=["Refrescar"])


@router_refrescar.put("/{fecha}", status_code=status.HTTP_200_OK, summary="Refresca los registros")
async def refrescarRegistros(fecha:str=Path(..., title="Fecha desde donde refrescar", description="Fecha con formato yyyy-mm-dd para refrescar"),
							payload:Payload=Depends(decodificarToken),
							con:Conexion=Depends(crearConexion))->Dict:

	"""
	Refresca los registros desde la fecha indicada incluida.

	Devuelve un mensaje de exito.

	## Parametros

	- **Fecha**: La fecha desde donde refrescar en formato yyyy-mm-dd (str).

	## Respuesta

	200 (OK): Si se refrescan los registros correctamente

	- **Mensaje**: El mensaje de actualizacion correcta de los registros (str).

	400 (BAD REQUEST): Si no se refrescan los registros correctamente

	- **Mensaje**: El mensaje de la excepcion (str).

	401 (UNAUTHORIZED): Si los datos no son correctos

	- **Mensaje**: El mensaje de la excepcion (str).
	"""

	try:

		fecha_datetime=datetime.datetime.strptime(fecha, "%Y-%m-%d")

		fecha_valida=Fecha.desdeDatetime(fecha_datetime)

	except ValueError:

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fecha formato incorrecto")

	except Exception:

		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fecha incorrecta")

	for mercado in ["españa", "portugal", "mibel"]:

		objeto_mercado=Mercado(mercado)

		con.eliminarRegistros(objeto_mercado.tabla, fecha_valida.fecha_str_formato)

		scraper=crearScraper(objeto_mercado)

		scraper.scrapear()

	return {"mensaje":f"Tablas refrescadas con exito desde {fecha_valida.fecha_str}"}