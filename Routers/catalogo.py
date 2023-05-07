from fastapi import APIRouter, Request, Depends, HTTPException, status
from DB.DB import coleccionProductos
from esquemas.esquemas import DatosProducto, productosEsquema

router = APIRouter(prefix="/productos", tags=["productos"], responses={404: {"message": "Sin productos registrados."}})

@router.get("/", response_model=list[DatosProducto])
async def listaProductos():
    return productosEsquema(coleccionProductos.find())