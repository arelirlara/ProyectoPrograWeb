from fastapi import APIRouter, Request, Depends, HTTPException, status
from DB.DB import coleccionSucursales
from esquemas.esquemas import DatosSucursales, sucursalesEsquema

router = APIRouter(prefix="/sucursales", tags=["sucursales"], responses={404: {"message": "Sin sucursales registrados."}})

@router.get("/", response_model=list[DatosSucursales])
async def listaSucursales():
    return sucursalesEsquema(coleccionSucursales.find())

@router.post("/nueva_sucursal",response_model= DatosSucursales ,status_code=201)
async def nuevoProducto(sucursal: DatosSucursales):
    if type(buscarSucursal("nombre", sucursal.nombre)) == DatosSucursales:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="La sucursal ya existe")
    
    diccionario_sucursal = dict(sucursal)
    del diccionario_sucursal["id"]

    id = coleccionSucursales.insert_one(diccionario_sucursal).inserted_id

    nueva_sucursal = sucursalesEsquema(coleccionSucursales.find_one({"_id": id}))

    return DatosSucursales((nueva_sucursal))

def buscarSucursal(field: str, key):
    try:
        sucursal = coleccionSucursales.find_one({field: key})
        return DatosSucursales(sucursalesEsquema(sucursal))
    except:
        return {"error": "No se ha encontrado sucursal."}