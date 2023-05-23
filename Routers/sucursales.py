from fastapi import APIRouter, Request, Depends, HTTPException, status
from DB.DB import coleccionSucursales
from esquemas.esquemas import DatosSucursales, sucursalesEsquema

router = APIRouter(prefix="/sucursales", tags=["sucursales"], responses={404: {"message": "Sin sucursales registrados."}})

@router.get("/", response_model=list[DatosSucursales])
async def listaSucursales():
    return sucursalesEsquema(coleccionSucursales.find())