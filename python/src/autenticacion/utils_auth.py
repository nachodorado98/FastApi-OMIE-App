from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import datetime

from .confauth import CLAVE, ALGORITMO
from src.modelos.token import Payload

# Funcion para generar el token unico del usuario
def generarToken(tiempo:int=30)->str:

    datos_token={"sub":"admin", "exp":datetime.datetime.utcnow()+datetime.timedelta(minutes=tiempo)}

    return jwt.encode(datos_token, key=CLAVE, algorithm=ALGORITMO)

# Funcion para decodificar el token unico del usuario
def decodificarToken(token:str=Depends(OAuth2PasswordBearer("/tokens")))->Payload:

    try:

        datos_token=jwt.decode(token, key=CLAVE, algorithms=[ALGORITMO])

        if datos_token["sub"]!="admin":

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado", headers={"WWW-Authentication":"Bearer"})

        return Payload(**datos_token)

    except JWTError as e:

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autorizado", headers={"WWW-Authentication":"Bearer"})