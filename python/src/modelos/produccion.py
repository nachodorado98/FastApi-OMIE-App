from pydantic import BaseModel

class Produccion(BaseModel):

    fecha:str
    hora:int
    carbon:float
    fuel_gas:float
    autoproductor:float
    nuclear:float
    hidraulica:float
    ciclo:float
    eolica:float
    solar_termica:float
    solar_fotovoltaica:float
    resto:float
    importacion_mibel:float
    importacion_sin_mibel:float