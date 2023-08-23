from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .utils_auth import generarToken

from src.modelos.token import Token


router_auth=APIRouter(tags=["Auth"])


@router_auth.post("/tokens", status_code=status.HTTP_200_OK, summary="Devuelve el token del admin")
async def obtenerToken(form:OAuth2PasswordRequestForm=Depends())->Token:

    """
    Devuelve el diccionario del token del admin.

    ## Respuesta

    200 (OK): Si los datos son correctos

    - **Access_token**: El token del admin (str).
    - **Token_type**: El tipo del token (str).

    401 (UNAUTHORIZED): Si los datos no son correctos

    - **Mensaje**: El mensaje de la excepcion (str).
    """

    if form.username!="admin" or form.password!="contrasena1234":

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Los datos son erroneos", headers={"WWW-Authentication":"Bearer"})       

    token=generarToken(30)

    return Token(access_token=token, token_type="bearer")