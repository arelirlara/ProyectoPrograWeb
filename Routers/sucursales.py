from fastapi import APIRouter, Request, Depends, HTTPException, status
from DB.DB import coleccionSucursales
from esquemas.esquemas import DatosSucursales, sucursalesEsquema
from bson import ObjectId

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

@router.put("/editar_sucursal", response_model=DatosSucursales)
async def user(sucursal: DatosSucursales):
        sucursal_diccionario = dict(sucursal)
        del sucursal_diccionario["id"]

        try:
            coleccionSucursales.find_one_and_replace({"_id": ObjectId(sucursal.id)}, sucursal_diccionario)
        except:
            return {"error": "No se ha actualizado el producto."}
        
        return buscarSucursal("_id", ObjectId(sucursal.id))

@router.delete("/eliminar_sucursal/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminarSucursal(id: str):
    encontrado = coleccionSucursales.find_one_and_delete({"_id": ObjectId(id)})

    if not encontrado:
        return {"error": "No se ha encontrado la sucursal."}

def buscarSucursal(field: str, key):
    try:
        sucursal = coleccionSucursales.find_one({field: key})
        return DatosSucursales(sucursalesEsquema(sucursal))
    except:
        return {"error": "No se ha encontrado sucursal."}